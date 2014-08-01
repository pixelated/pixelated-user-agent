
# Very simple search for contacts. The search string will be something that will be prefix matched
# using a boundary before but not after. If you put in more than one word, those two will be searched
# and ANDed together. You can use double quotes or single quotes to do the obvious thing instead
module PixelatedService
  class ContactsSearch
    def initialize(q)
      @qtree = ContactsSearch.compile(q)
    end

    def restrict(input)
      input.select do |mm|
        @qtree.match?(mm)
      end
    end

    REGEXP_DQUOTED = /"[^"]*"/
    REGEXP_SQUOTED = /'[^']*'/
    REGEXP_OTHER = /[^\s]+/

    class AndMatch
      attr_reader :data
      def initialize(data = [])
        @data = data
      end
      def <<(node)
        @data << node
      end
      def match?(c)
        self.data.all? { |mm| mm.match?(c) }
      end
    end

    class StringMatch
      def initialize(data, quoted=false)
        @data = Regexp.new(Regexp.quote(if quoted
                                          data[1..-2]
                                        else
                                          data
                                        end), Regexp::IGNORECASE)
        @exact_match = /\b#{@data}/
      end

      def match_string?(str)
        Array(str).any? { |ff| @exact_match.match ff }
      end

      def match?(c)
        match_string? ([c.name] + c.addresses.to_a).compact
      end
    end

    def self.compile(q)
      qs = StringScanner.new(q)
      qtree = AndMatch.new
      until qs.eos?
        res =
          if qs.check(REGEXP_DQUOTED)
            StringMatch.new(qs.scan(REGEXP_DQUOTED), true)
          elsif qs.check(REGEXP_SQUOTED)
            StringMatch.new(qs.scan(REGEXP_SQUOTED), true)
          elsif qs.check(REGEXP_OTHER)
            StringMatch.new(qs.scan(REGEXP_OTHER))
          end
        qtree << res
        qs.scan(/\s+/)
      end
      qtree
    end
  end
end
