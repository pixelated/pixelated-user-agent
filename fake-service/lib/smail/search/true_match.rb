module Smail
  class Search
    class TrueMatch
      def match?(mail)
        true
      end

      def match_string?(str)
        true
      end
    end
  end
end
