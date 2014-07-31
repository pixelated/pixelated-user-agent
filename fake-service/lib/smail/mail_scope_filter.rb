module Smail
  module MailScopeFilter
    include Enumerable

    def initialize(c)
      @c = c
    end

    def each
      @c.each do |m|
        yield m if retain?(m)
      end
    end

    class Default
      include MailScopeFilter

      def initialize(c)
        super
        @tags = [Tags.get('sent'), Tags.get('trash'), Tags.get('drafts')]
      end

      def retain?(m)
        !(@tags.any? { |t| m.is_tagged?(t) })
      end

      class << self
        def +(o)
          o
        end
      end
    end

    class All
      include MailScopeFilter

      def initialize(c)
        super
        @t = Tags.get('trash')
      end

      def retain?(m)
        !m.is_tagged?(@t)
      end

      class << self
        def +(o)
          All
        end
      end
    end

    def self.tagged_with(n)
      t = Tags.get(n)
      c = Class.new
      c.send :include, MailScopeFilter
      c.send :define_method, :retain? do |m|
        m.is_tagged?(t)
      end
      c.class.send :define_method, :+ do |o|
        All === o ? All : self
      end
      c
    end

    Trash  = tagged_with('trash')
    Sent   = tagged_with('sent')
    Drafts = tagged_with('drafts')
  end
end
