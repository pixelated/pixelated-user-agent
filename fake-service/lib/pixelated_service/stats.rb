
module PixelatedService
  module Stats
    class StatsCollector
      include Stats
      def initialize
        stats_init
      end
    end

    attr_reader :stats

    def stats_init
      @stats = {
        total: 0,
        read: 0,
        starred: 0,
        replied: 0
      }
    end

    def stats_added(m)
      @stats[:total] += 1
      stats_status_added(:read, m)    if m.status?(:read)
      stats_status_added(:replied, m) if m.status?(:replied)
      stats_status_added(:starred, m) if m.status?(:starred)
    end

    def stats_removed(m)
      @stats[:total] -= 1
      stats_status_removed(:read, m)    if m.status?(:read)
      stats_status_removed(:replied, m) if m.status?(:replied)
      stats_status_removed(:starred, m) if m.status?(:starred)
    end

    def stats_status_added(s, m)
      @stats[s] += 1
    end

    def stats_status_removed(s, m)
      @stats[s] -= 1
    end

    def each_total_helper(enum)
      if enum.respond_to?(:each_total)
        enum.each_total { |x| yield x }
      else
        enum.each { |x| yield x }
      end
    end

    def with_stats(enum)
      sc = StatsCollector.new
      each_total_helper(enum) do |e|
        sc.stats_added(e)
      end
      [sc.stats, enum]
    end
  end
end
