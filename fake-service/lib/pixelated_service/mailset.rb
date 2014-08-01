require 'set'

module PixelatedService
  class Mailset
    DIR = File.expand_path File.join(File.dirname(__FILE__), "..", "..", "data", "mail-sets")

    class << self
      def create(name, number, tagging)
        ms = new name, number, tagging, nil
        ms.generate!
        ms
      end

      def load(name, observers)
        ms = new(name, -1, nil, observers)
        if ms.load!
          ms
        else
          nil
        end
      end
    end

    attr_reader :mails
    attr_reader :tags

    def initialize(name, number, tagging, observers)
      @name, @number, @tagging, @observers = name, number, tagging, observers
    end

    def generate!
      @persona = Generator.random_persona
      @tags = Generator.tags(Generator.ladder_distribution(4, 40))

      @mails = {}
      @tags = Set.new
      (0...(@number)).each do |i|
        res = if @tagging
                Generator.random_tagged_mail(@tags)
              else
                Generator.random_mail
              end
        @observers.mail_added res
        @tags.merge res.tags
        res.ident = i
        @mails[res.ident] = res
      end
    end

    def save!
      dir = File.join(DIR, @name)
      Dir.mkdir(dir) unless Dir.exists?(dir)
      File.open(File.join(dir, "persona.yml"), "w") do |f|
        f.write @persona.to_yaml
      end

      @mails.each do |(k, m)|
        nm = "mbox%08x" % m.ident
        File.open(File.join(dir, nm), "w") do |f|
          f.write m.to_s
        end
      end
    end

    def load!
      dir = File.join(DIR, @name)
      return false unless Dir.exists?(dir)
      @persona = YAML.load_file(File.join(dir, "persona.yml"))
      @mails = {}
      @ix = 0
      Dir["#{dir}/mbox*"].each do |f|
        File.open(f) do |fio|
          res = PixelatedService::Mail.read fio, @ix
          res.read = true if (res.tag_names.include?('sent') || res.tag_names.include?('drafts'))
          @mails[res.ident] = res
          @observers.mail_added res
          res.security_casing = SecurityCasingExamples::Case.case_from(res.ident.to_i)
          @ix += 1
        end
      end
      true
    end
  end
end
