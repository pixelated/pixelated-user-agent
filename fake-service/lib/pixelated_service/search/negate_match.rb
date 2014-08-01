module PixelatedService
  class Search
    class NegateMatch
      attr_reader :data
      def initialize(data)
        @data = data
      end

      def to_s
        "Negate(#@data)"
      end

      def match?(mail)
        !self.data.match?(mail)
      end

      def match_string?(str)
        !self.data.match_string?(str)
      end
    end
  end
end
