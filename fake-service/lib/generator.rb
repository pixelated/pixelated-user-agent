require 'faker'

I18n.enforce_available_locales = true
Faker::Config.locale = 'en-us'

module Generator
  TAGS = File.read(File.join(File.dirname(__FILE__), "..", "data", "tags")).split.map { |tt| tt.chomp }
  module Mail
    def random_header
      {
        from: Faker::Internet.email,
        to: Faker::Internet.email,
        subject: Faker::Lorem.sentence
      }
    end

    def random_body
      Faker::Lorem.paragraphs.join("\n\n")
    end

    extend Mail
  end

  def tag
    TAGS.sample
  end

  def ladder_distribution(from, to, factor = 1)
    mid = from + ((to - from) / 2)
    result = []
    curr = 1
    direction = 1
    (from..to).each do |i|
      result.concat [i] * curr
      if i == mid
        direction = -1
      end
      curr += (direction * factor)
    end
    result
  end

  def choose(distribution)
    case distribution
    when Integer
      distribution
    when Range
      rand((distribution.last+1) - distribution.first) + distribution.first
    when Array
      choose(distribution.sample)
    end
  end

  def tags(distribution = 3)
    num = choose(distribution)
    num.times.map { self.tag }
  end

  def random_mail
    hdr = Mail.random_header
    bd = Mail.random_body
    PixelatedService::Mail.new(
                    from: hdr[:from],
                    to: hdr[:to],
                    subject: hdr[:subject],
                    body: bd
                    )
  end

  def random_tagged_mail(tagset)
    hdr = Mail.random_header
    bd = Mail.random_body
    tgs = choose(ladder_distribution(1, 5)).times.map { tagset.sample }.uniq
    special_tag = ([nil, nil, nil, nil, nil, nil] + PixelatedService::Tags::SPECIAL).sample
    status = []
    status << :read if special_tag == 'sent'
    mail = PixelatedService::Mail.new(
                    from: hdr[:from],
                    to: hdr[:to],
                    subject: hdr[:subject],
                    body: bd,
                    tags: (tgs + Array(special_tag)).compact,
                    status: status
                    )
    mail
  end

  def random_persona
    PixelatedService::Persona.new(Faker::Number.number(10),
                       Faker::Name.name,
                       Faker::Lorem.sentence,
                       Faker::Internet.email)
  end

  extend Generator
end
