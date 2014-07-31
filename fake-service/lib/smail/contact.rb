
module Smail
  class Contact < Struct.new(:ident, :name, :addresses, :mails_received, :mails_sent, :last_received, :last_sent, :prev, :next)
    include Comparable

    def to_json(*args)
      {
        ident: self.ident,
        name: self.name,
        addresses: Array(self.addresses),
        mails_received: self.mails_received || 0,
        mails_sent: self.mails_sent || 0,
        last_received: self.last_received,
        last_sent: self.last_sent
      }.to_json(*args)
    end

    def comparison_value
      [(self.mails_received || 0) + (self.mails_sent || 0) * 0.8, self.last_received, self.last_sent]
    end

    def <=>(other)
      other.comparison_value <=> self.comparison_value
    end
  end
end
