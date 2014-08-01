module PixelatedService
  class CombinedObserver
    def initialize(*observers)
      @observers = observers
    end

    def <<(observer)
      @observers << observer
    end

    def mail_added(mail)
      @observers.each { |o| o.mail_added(mail) }
    end

    def mail_removed(mail)
      @observers.each { |o| o.mail_removed(mail) }
    end

    def mail_updated(before, after)
      @observers.each { |o| o.mail_updated(before, after) }
    end
  end
end
