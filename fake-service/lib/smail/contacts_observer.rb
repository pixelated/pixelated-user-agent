module Smail
  class ContactsObserver
    def initialize(contacts)
      @contacts = contacts
    end

    def extract_addresses(*addrs)
      addrs.flatten.compact
    end

    def all_receivers(mail, &block)
      extract_addresses(mail.to, mail.cc, mail.bcc).each(&block)
    end

    def all_senders(mail, &block)
      extract_addresses(mail.from).each(&block)
    end

    def new_receivers(before, after, &block)
      (extract_addresses(after.to, after.cc, after.bcc) - extract_addresses(before.to, before.cc, before.bcc)).each(&block)
    end

    def new_senders(before, after, &block)
      (extract_addresses(after.from) - extract_addresses(before.from)).each(&block)
    end

    def timestamp_from(mail)
      mail.headers[:date]
    end

    def mail_added(mail)
      timestamp = timestamp_from(mail)
      all_receivers(mail) do |rcv|
        @contacts.new_mail_to(rcv, timestamp)
      end
      all_senders(mail) do |s|
        @contacts.new_mail_from(s, timestamp)
      end
    end

    def mail_removed(mail)
    end

    def mail_updated(before, after)
      timestamp = timestamp_from(after)
      new_receivers(before, after) do |rcv|
        @contacts.new_mail_to(rcv, timestamp)
      end
      new_senders(before, after) do |s|
        @contacts.new_mail_from(s, timestamp)
      end
    end
  end
end
