module Smail
  class Search
    class StringMatch
      attr_reader :str
      def initialize(data, quoted=false)
        @str = data
        @quoted = quoted
        @data = Regexp.new(Regexp.quote(self.match_string), Regexp::IGNORECASE)
        @exact_match = /^#{@data}$/
      end

      def match_string
        if @quoted
          @str[1..-2]
        else
          @str
        end
      end

      def to_s
        "String(#@data)"
      end

      def match_string?(str)
        Array(str).any? { |ff| !!(ff[@data]) }
      end

      def match_exact_string?(str)
        Array(str).any? { |ff| @exact_match.match ff }
      end

      def match?(mail)
        match_string? [mail.to, mail.from, mail.subject, mail.body]
      end
    end
  end
end
