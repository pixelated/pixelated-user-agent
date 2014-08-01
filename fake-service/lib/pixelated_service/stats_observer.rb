module PixelatedService
  class StatsObserver
    def initialize(stats)
      @stats = stats
      @stats.stats_init
    end

    def mail_added(mail)
      @stats.stats_added mail
    end

    def mail_removed(mail)
      @stats.stats_removed mail
    end

    def mail_updated(before, after)
    end
  end
end
