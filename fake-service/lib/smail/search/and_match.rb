module Smail
  class Search
    class AndMatch
      attr_reader :data
      def initialize(data = [])
        @data = data
      end
      def <<(node)
        @data << node
      end

      def to_s
        "And(#{@data.join(", ")})"
      end

      def match?(mail)
        self.data.all? { |mm| mm.match?(mail) }
      end

      def match_string?(str)
        self.data.all? { |mm| mm.match_string?(str) }
      end
    end
  end
end
