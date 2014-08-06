module PixelatedService
  class Mail
    attr_reader :to, :cc, :bcc, :from, :subject, :body, :headers, :status, :draft_reply_for
    attr_accessor :ident, :security_casing

    def initialize(data = {})
      @ident = data[:ident]
      @to = data[:to]
      @cc = data[:cc]
      @bcc = data[:bcc]
      @from = data[:from]
      @subject = data[:subject]
      @body = data[:body]
      @headers = data[:headers] || {}
      @status = data[:status] || []
      @draft_reply_for = data[:draft_reply_for] || []
      self.tags = data[:tags] || Tags.new
    end

    def hash
      @ident.hash
    end

    def eql?(object)
      self == object
    end

    def tags=(t)
      @tags.mail = nil if @tags
      @tags = t
      @tags.mail = self if @tags
      t
    end

    def ==(object)
      @ident == object.ident
    end

    def tag_names
      @tags.names
    end

    def is_tagged?(t)
      @tags.is_tagged?(t)
    end

    def tag_names=(vs)
      to_remove = self.tag_names - vs
      to_add = vs - self.tag_names

      to_remove.each do |tn|
        self.remove_tag(tn)
      end

      to_add.each do |v|
        self.add_tag(v)
      end
    end

    def add_tag(nm)
      @tags.add_tag(nm)
    end

    def remove_tag(nm)
      @tags.remove(nm)
    end

    def has_trash_tag?
      tag_names.include? "trash"
    end

    def starred=(v); v ? add_status(:starred) : remove_status(:starred); end
    def starred?; status?(:starred); end
    def read=(v); v ? add_status(:read) : remove_status(:read); end
    def read?; status?(:read); end
    def replied=(v); v ? add_status(:replied) : remove_status(:replied); end
    def replied?; status?(:replied); end

    def add_status(n)
      unless self.status?(n)
        @status = @status + [n]
        @tags.added_status(n)
        PixelatedService.mail_service.stats_status_added(n, self)
      end
    end

    def remove_status(n)
      if self.status?(n)
        @status = @status - [n]
        @tags.removed_status(n)
        PixelatedService.mail_service.stats_status_removed(n, self)
      end
    end

    def status?(n)
      @status.include?(n)
    end

    def to_json(*args)
      {
        header: {
          to: Array(@to),
          from: @from,
          subject: @subject,
        }.merge(@headers).merge({date: @headers[:date].iso8601}),
        ident: ident,
        tags: @tags.names,
        status: @status,
        security_casing: @security_casing,
        draft_reply_for: @draft_reply_for,
        body: @body
      }.to_json(*args)
    end


    def self.from_json(obj, new_ident = nil)
      ident = obj['ident']
      draft_reply_for = obj['draft_reply_for']
      hdrs = obj['header']
      to = hdrs['to']
      cc = hdrs['cc']
      bcc = hdrs['bcc']
      from = hdrs['from']
      subject = hdrs['subject']
      new_hdrs = {}
      hdrs.each do |k,v|
        new_hdrs[k.to_sym] = v unless %w(from to subject).include?(k)
      end
      tag_names = obj['tags']
      st = obj['status']
      bd = obj['body']

      mail = new(:subject => subject,
          :from => from,
          :to => Array(to),
          :cc => Array(cc),
          :bcc => Array(bcc),
          :headers => new_hdrs,
          :status => st,
          :draft_reply_for => draft_reply_for,
          :ident => (ident.to_s.empty? ? new_ident : ident),
          :body => bd)

      tag_names.each do |tag_name|
        mail.add_tag tag_name
      end

      mail

    end

    def to_s
      ([
        ("#{INTERNAL_TO_EXTERNAL_HEADER[:to]}: #{format_header_value_out(:to, @to)}" if @to),
        ("#{INTERNAL_TO_EXTERNAL_HEADER[:from]}: #{format_header_value_out(:from, @from)}" if @from),
        ("#{INTERNAL_TO_EXTERNAL_HEADER[:subject]}: #{format_header_value_out(:subject, @subject)}" if @subject),
        ("#{INTERNAL_TO_EXTERNAL_HEADER[:x_tw_pixelated_tags]}: #{format_header_value_out(:x_tw_smail_tags, @tags.names)}" if !@tags.names.empty?),
        ("#{INTERNAL_TO_EXTERNAL_HEADER[:x_tw_pixelated_status]}: #{format_header_value_out(:x_tw_smail_status, @status)}" if !@status.empty?),
        ("#{INTERNAL_TO_EXTERNAL_HEADER[:x_tw_pixelated_ident]}: #{format_header_value_out(:x_tw_smail_ident, @ident)}"),
       ].compact + @headers.map { |k,v| "#{INTERNAL_TO_EXTERNAL_HEADER[k]}: #{format_header_value_out(k, v)}"}).sort.join("\n") + "\n\n#{@body}"
    end

    SPECIAL_HEADERS = [:subject, :from, :to, :x_tw_pixelated_tags, :x_tw_smail_status, :x_tw_smail_ident]
    INTERNAL_TO_EXTERNAL_HEADER = {
      :subject => "Subject",
      :date => "Date",
      :from => "From",
      :to => "To",
      :cc => "CC",
      :bcc => "BCC",
      :message_id => "Message-ID",
      :mime_version => "Mime-Version",
      :content_type => "Content-Type",
      :content_transfer_encoding => "Content-Transfer-Encoding",
      :x_tw_pixelated_tags => "X-TW-Pixelated-Tags",
      :x_tw_pixelated_status => "X-TW-Pixelated-Status",
      :x_tw_pixelated_ident => "X-TW-Pixelated-Ident",
    }

    def format_header_value_out(k,v)
      case k
      when :date
        v.strftime("%a, %d %b %Y %H:%M:%S %z")
      when :to, :cc, :bcc
        Array(v).join(", ")
      when :x_tw_pixelated_tags, :x_tw_smail_status
        v.join(", ")
      else
        v
      end
    end

    class << self
      def formatted_header(k, ls)
        format_header_value(k, ls[k] && ls[k][1])
      end

      def has_header(hdr_name, ls, val, otherwise)
        if ls[hdr_name]
          val
        else
          otherwise
        end
      end

      def time_rand from = (Time.now - 300000000), to = Time.now
        Time.at(from + rand * (to.to_f - from.to_f))
      end

      # io is String or IO
      def read(io, ident = nil)
        io = StringIO.new(io) if io.is_a? String
        headers = {}
        body = ""
        reading_headers = true
        previous_header = nil
        first = true
        io.each do |ln|
          if first && ln =~ /^From /
            # Ignore line delimiter things
          else
            if reading_headers
              if ln.chomp == ""
                reading_headers = false
              else
                if previous_header && ln =~ /^\s+/
                  previous_header[1] << " #{ln.strip}"
                else
                  key, value = ln.chomp.split(/: /, 2)
                  previous_header = [key, value]
                  headers[internal_header_name(key)] = previous_header
                end
              end
            else
              body << ln
            end
          end
          if first
            first = false
          end
        end

        header_data = {}
        headers.each do |k, (_, v)|
          unless special_header?(k)
            header_data[k] = format_header_value(k, v)
          end
        end

        unless header_data[:date]
          header_data[:date] = time_rand
        end


        new(:subject => formatted_header(:subject, headers),
            :from => formatted_header(:from, headers),
            :to => formatted_header(:to, headers),
            :headers => header_data,
            :tags => formatted_header(:x_tw_pixelated_tags, headers),
            :status => formatted_header(:x_tw_pixelated_status, headers),
            :ident => has_header(:x_tw_pixelated_ident, headers, formatted_header(:x_tw_smail_ident, headers), ident),
            :body => body
            )
      end


      private
      def internal_header_name(k)
        k.downcase.gsub(/-/, '_').to_sym
      end

      def special_header?(k)
        SPECIAL_HEADERS.include?(k)
      end

      def format_header_value(k, v)
        case k
        when :date
          DateTime.parse(v)
        when :to, :cc, :bcc
          vs = (v || "").split(/, /)
          if vs.length == 1
            vs[0]
          else
            vs
          end
        when :x_tw_pixelated_tags
          Tags.new *(v || "").split(/, /)
        when :x_tw_pixelated_status
          (v || "").split(/, /).map { |ss| ss.to_sym }
        when :x_tw_pixelated_ident
          v.to_i
        else
          v
        end
      end
    end
  end
end
