module PixelatedService
  class Tag < Struct.new(:name, :total_count, :read, :starred, :replied, :default)
    def to_json(*args)
      {
        name: self.name,
        ident: self.name.hash.abs,
        default: self.default,
        counts: {
          total: self.total_count,
          read: self.read,
          starred: self.starred,
          replied: self.replied,
        }
      }.to_json(*args)
    end
  end

  class Tags
    SPECIAL = %w(inbox sent drafts trash)

    def initialize(*desired_names)
      @tags = desired_names.each_with_object({}) do |name, res|
        res[normalized(name)] = Tags.get(name)
      end
    end

    def increase_all_count(t = nil)
      change_all_count 1, t, :total_count
    end

    def decrease_all_count(t = nil)
      change_all_count -1, t, :total_count
    end

    def change_all_count(v, t, s)
      tags = t ? [t] : @tags.values
      tags.each do |tag|
        tag[s] += v
      end
    end

    def increase_status_count_checked(status, t = nil)
      increase_status_count status, t if @mail.status?(status)
    end

    def decrease_status_count_checked(status, t = nil)
      decrease_status_count status, t if @mail.status?(status)
    end

    def increase_status_count(status, t = nil)
      change_all_count 1, t, status
    end

    def decrease_status_count(status, t = nil)
      change_all_count -1, t, status
    end

    def decrease_all(t = nil)
      decrease_all_count  t
      decrease_status_count_checked :read, t
      decrease_status_count_checked :starred, t
      decrease_status_count_checked :replied, t
    end

    def increase_all(t = nil)
      increase_all_count  t
      increase_status_count_checked :read, t
      increase_status_count_checked :starred, t
      increase_status_count_checked :replied, t
    end

    def mail=(m)
      decrease_all  if @mail
      @mail = m
      increase_all  if m
    end

    def add_tag(name)
      unless @tags[normalized(name)]
        t = @tags[normalized(name)] = Tags.get(name)
        increase_all t
      end
    end

    def remove(name)
      if t = @tags[normalized(name)]
        @tags.delete(normalized(name))
        decrease_all t
      end
    end

    def added_status(nm)
      increase_status_count nm
    end

    def removed_status(nm)
      decrease_status_count nm
    end

    def is_tagged?(t)
      !!@tags[normalized(t.name)]
    end

    def names
      @tags.values.sort_by do |v|
        [SPECIAL.index(normalized(v.name)) || 999, normalized(v.name)]
      end.map(&:name)
    end

    def normalized(n)
      Tags.normalized(n)
    end

    class <<self
      def normalized(n)
        n.downcase
      end

      def get(name)
        self.tags[normalized(name)] || create_tag(name)
      end

      def tags
        @tags ||= {}
      end

      def clean
        @tags = {}
        create_default_tags
        @tags
      end

      def all_tags
        tags.values.sort_by { |x| normalized(x.name) }
      end

      def create_tag(name)
        PixelatedService::Tag.new(name, 0, 0, 0, 0, false).tap do |t|
          self.tags[normalized(name)] = t
        end
      end

      def create_default_tags()
        SPECIAL.each do |name|
          self.tags[normalized(name)] = PixelatedService::Tag.new(name, 0, 0, 0, 0, true)
        end
      end
    end
  end
end
