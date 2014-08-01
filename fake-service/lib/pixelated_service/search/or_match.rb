module PixelatedService
  class Search
    class OrMatch
      attr_reader :left, :right
      def initialize(left, right)
        @left = left
        @right = right
      end
      def <<(node)
        @right << node
      end
      def to_s
        "Or(#@left, #@right)"
      end

      def match?(mail)
        [@left, @right].any? { |mm| mm.match?(mail) }
      end

      def match_string?(str)
        [@left, @right].any? { |mm| mm.match_string?(str) }
      end
    end
  end
end
