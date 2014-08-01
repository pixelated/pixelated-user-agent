
module PixelatedService
  class Paginate
    def initialize(page, window_size)
      @start = page * window_size
      @end   = (page + 1) * window_size
    end

    def restrict(input)
      PaginatedEnumerable.new(input, @start, @end)
    end
  end
end

require 'pixelated_service/paginated_enumerable'
