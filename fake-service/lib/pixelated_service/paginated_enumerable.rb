
module PixelatedService
  class Paginate
    class PaginatedEnumerable
      include Enumerable
      def initialize(input, start, e)
        @input = input
        @start = start
        @end = e
      end

      def each
        @input.each_with_index do |v, ix|
          if ix >= @end
            return #we are done
          elsif ix >= @start
            yield v
          end
        end
      end

      def each_total
        @input.each do |v|
          yield v
        end
      end
    end
  end
end
