module PixelatedService
  class SortedMail
    include Enumerable

    NEWEST_FIRST = lambda do |l,r|
        (r.headers[:date] || Time.now) <=> (l.headers[:date] || Time.now)
    end

    def initialize(&block)
      @mails = {}
      @mail_order = []
      @sort_procedure = block || NEWEST_FIRST
    end

    def []=(k, v)
      @mails[k] = v
      @mail_order << v
      sort_mail_order!
      v
    end

    def [](k)
      @mails[k]
    end

    def delete(k)
      v = @mails.delete(k)
      @mail_order.delete(v)
      v
    end

    def add_all(hs)
      hs.each do |h,v|
        @mails[h] = v
        @mail_order << v
      end
      sort_mail_order!
      self
    end

    def length
      @mails.length
    end

    def sort_mail_order!
      @mail_order.sort!(&@sort_procedure)
      @mail_order.compact!
      @mail_order.uniq!
    end

    def each
      @mail_order.each do |m|
        yield m
      end
    end
  end
end
