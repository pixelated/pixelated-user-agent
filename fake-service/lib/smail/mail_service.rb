require 'set'

module Smail
  class MailService
    include Enumerable
    include Smail::Stats

    def each
      @mails.each do |mo|
        yield mo
      end
    end

    def initialize
      self.clean
    end

    def contact(ix)
      @contacts.contact(ix)
    end

    def contacts
      @contacts.to_a
    end

    def clean
      Smail::Tags.clean
      @next_ident = 0
      @reply_drafts = {}
      @mails = SortedMail.new
      @contacts = Contacts.new(Fake::PERSONAS[0])
      @observers = CombinedObserver.new(StatsObserver.new(self),
                                        ContactsObserver.new(@contacts))
    end

    def create(mail=Generator.random_mail)
      unless mail.ident
        mail.ident = @next_ident
        @next_ident += 1
      end
      @mails[mail.ident] = mail
      @observers.mail_added(mail)
    end

    def create_tag(tag_json)
      Smail::Tags.create_tag tag_json['tag']
    end

    def mail(ix)
      @mails[ix.to_i]
    end

    def send_mail(data)
      ms = Mail.from_json(data, @next_ident)
      if ms.tag_names.include?("sent")
        ms.remove_tag "drafts"
        @reply_drafts.delete ms.draft_reply_for
      elsif ms.tag_names.include?("drafts") and ms.draft_reply_for
        @reply_drafts[ms.draft_reply_for] = ms.ident
      end
      @next_ident += 1
      @mails[ms.ident] = ms
      update_status ms
      @observers.mail_added(ms)
      ms.ident
    end

    def draft_reply_for(ident)
      @mails[@reply_drafts[ident.to_i]]
    end

    def update_mail(data)
      mail = Mail.from_json(data)
      before = @mails[mail.ident]
      @mails[mail.ident] = mail
      update_status mail
      @observers.mail_updated(before, mail)
      before.tags = nil
      mail.ident
    end

    def update_status(mail)
      mail.read = true
      mail.headers[:date] = Time.now
    end

    def tags(q)
      if q && !q.strip.empty?
        query = /\b#{Regexp.new(Regexp.quote(q), Regexp::IGNORECASE)}/
        Smail::Tags.all_tags.select do |tt|
          query =~ tt.name
        end
      else
        Smail::Tags.all_tags
      end
    end

    def stats_report
      { stats: self.stats }
    end

    def delete_mail(ix)
      ms = @mails[ix.to_i]
      @reply_drafts.delete ms.draft_reply_for

      if ms.has_trash_tag?
        m = @mails.delete ix.to_i
        @observers.mail_removed(m)
        m.tags = nil
      else
        ms.add_tag 'trash'
      end
    end

    def load_mailset(name)
      self.clean
      ms = Smail::Mailset.load(name, @observers)
      raise "couldn't find mailset #{name}" unless ms
      @mails.add_all ms.mails
      self.stats
    end

    def mails(q, page, window_size)
      restrictors = [All.new]
      restrictors << Paginate.new(page, window_size) if window_size > 0
      restrictors << Search.new(q)
      with_stats(restrictors.reverse.inject(self) do |ms, restr|
        restr.restrict(ms)
      end)
    end

    def contacts(q, page, window_size)
      restrictors = [All.new]
      restrictors << ContactsSorter.new
      restrictors << Paginate.new(page, window_size) if window_size > 0
      restrictors << ContactsSearch.new(q) if q
      restrictors.reverse.inject(@contacts) do |c, restr|
        restr.restrict(c)
      end
    end

    def delete_mails(q, page, window_size, idents=nil)
      unless idents.nil?
        @mails.each { |k,v| delete_mail(k.ident) if idents.include?(k.ident) }
      else
        mails(q, page, window_size).each do |m|
          delete_mail m.ident
        end
      end
    end
  end
end
