require 'open-uri'
require 'archive/tar/minitar'
require 'fileutils'

module PixelatedService
  class << self
    def mail_service
      @mail_service ||= MailService.new
    end
  end

  module Fake
    PERSONAS = [
      Persona.new(1, "Yago Macedo", nil, "sirineu@souza.org")
    ]

    def personas
      PERSONAS.map(&:ident)
    end

    def persona(i)
      PERSONAS.select { |x| x.ident.to_s == i}.first
    end

    def mails(query, page_number, window_size)
      with_timing do
        stats, mails = PixelatedService.mail_service.mails(query, page_number, window_size)
        { stats: stats, mails: mails.to_a }
      end
    end

    def contacts(query, page_number, window_size)
      with_timing do
        contacts = PixelatedService.mail_service.contacts(query, page_number, window_size)
        { contacts: contacts.to_a }
      end
    end

    def contact(ix)
      PixelatedService.mail_service.contact(ix)
    end

    def delete_mails(query, page_number, window_size, mails_idents)
      idents = mails_idents.gsub(/[\[\]]/, '').split(',').collect {|x| x.to_i}
      PixelatedService.mail_service.delete_mails(query, page_number, window_size, idents)
      []
    end

    def mail(i)
      PixelatedService.mail_service.mail(i)
    end

    def send_mail(data)
      PixelatedService.mail_service.send_mail(data)
    end

    def update_mail(data)
      PixelatedService.mail_service.update_mail(data)
    end

    def delete_mail(i)
      PixelatedService.mail_service.delete_mail(i)
    end

    def draft_reply_for(i)
      PixelatedService.mail_service.draft_reply_for(i)
    end

    def tags(i)
      PixelatedService.mail_service.mail(i).tag_names
    end

    def create_tag(tag_json)
      PixelatedService.mail_service.create_tag tag_json
    end

    def all_tags(q)
      PixelatedService.mail_service.tags(q)
    end

    def settags(i, body)
      m = PixelatedService.mail_service.mail(i)
      m.tag_names = body["newtags"]
      m.tag_names
    end

    def starmail(i, val)
      m = PixelatedService.mail_service.mail(i)
      m.starred = val if m
      ""
    end

    def repliedmail(i, val)
      m = PixelatedService.mail_service.mail(i)
      m.replied = val if m
      ""
    end

    def readmail(i, val)
      m = PixelatedService.mail_service.mail(i)
      m.read = val if m
      ""
    end

    def readmails(mail_idents, val)
      idents = mail_idents.gsub(/[\[\]]/, '').split(',').collect {|x| x.to_i}
      PixelatedService.mail_service.each { |k,v| readmail(k.ident, val) if idents.include?(k.ident) }
      []
    end

    def control_create_mail
      PixelatedService.mail_service.create
      ""
    end

    def control_delete_mails
      PixelatedService.mail_service.clean
      ""
    end

    def control_mailset_load(name)
      mbox_root = 'data/mail-sets/'
      if (Dir["#{mbox_root}/mbox*"].empty?)

        FileUtils.mkdir_p(mbox_root)
        unless (File.exists?("#{mbox_root}/mediumtagged.tar.gz"))
          medium_tagged = File.new("#{mbox_root}/mediumtagged.tar.gz", 'w')
          web_medium_tagged = open('https://example.wazokazi.is:8154/go/static/mediumtagged.tar.gz', :ssl_verify_mode => OpenSSL::SSL::VERIFY_NONE)
          medium_tagged.write(web_medium_tagged.read)
          medium_tagged.close
        end
        Archive::Tar::Minitar.unpack("#{mbox_root}/mediumtagged.tar.gz", mbox_root)
      end

      with_timing do
        {
          stats: PixelatedService.mail_service.load_mailset(name),
          loaded: name
        }
      end
    end

    def stats
      PixelatedService.mail_service.stats_report
    end

    def with_timing
      before = Time.now
      result = yield
      after = Time.now
      res = case result
            when Hash
              result.dup
            when nil
              {}
            else
              { result: result }
            end
      res[:timing] = { duration: after - before }
      res
    end
  end
end
