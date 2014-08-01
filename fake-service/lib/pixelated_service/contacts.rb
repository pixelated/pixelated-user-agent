require 'mail'
require 'set'

module PixelatedService
  class Contacts
    include Enumerable

    def initialize(persona)
      @persona = persona
      @contacts = nil
      @contacts_cache = {}
      @contacts_lookup = {}
    end

    def contact(ix)
      @contacts_lookup[ix]
    end

    def each
      curr = @contacts
      while curr
        yield curr
        curr = curr.next
      end
    end

    def normalize(addr)
      addr.downcase
    end

    def parse(a)
      ::Mail::Address.new(a)
    end

    def update c, addr
      @contacts_cache[normalize(addr.address)] = c
      c.name = addr.display_name if addr.display_name
      (c.addresses ||= Set.new) << addr.address
    end

    def create_new_contact(addr)
      old_first = @contacts
      c = Contact.new
      c.ident = addr.hash.abs.to_s
      c.next = old_first
      @contacts_lookup[c.ident] = c
      @contacts = c
      update c, addr
      c
    end

    def find_or_create(addr)
      parsed = parse(addr)
      if cc = @contacts_cache[normalize(parsed.address)]
        update cc, parsed
        cc
      else
        create_new_contact(parsed)
      end
    end

    def latest(prev, n)
      if prev && prev > n
        prev
      else
        n
      end
    end

    def new_mail_from(a, t)
      contact = find_or_create(a)
      contact.last_received = latest(contact.last_received, t)
      contact.mails_received ||= 0
      contact.mails_received += 1
    end

    def new_mail_to(a, t)
      contact = find_or_create(a)
      contact.last_sent = latest(contact.last_sent, t)
      contact.mails_sent ||= 0
      contact.mails_sent += 1
    end
  end
end
