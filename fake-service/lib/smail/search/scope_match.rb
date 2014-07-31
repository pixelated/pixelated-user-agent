
module Smail
  class Search
    class ScopeMatch
      def initialize(scope, data)
        @scope = scope.downcase.gsub(/-/, '_').to_sym
        @data = data
      end

      def to_s
        "Scope(#@scope, #@data)"
      end

      def is_search_scope?
        [:in, :tag, :is].include?(@scope) &&
          %w(_default_ trash all sent drafts).include?(@data.match_string.downcase)
      end

      def search_scope
        case @data.match_string.downcase
        when '_default_'
          Smail::MailScopeFilter::Default
        when 'all'
          Smail::MailScopeFilter::All
        when 'trash'
          Smail::MailScopeFilter::Trash
        when 'sent'
          Smail::MailScopeFilter::Sent
        when 'drafts'
          Smail::MailScopeFilter::Drafts
        end
      end

      def match?(mail)
        strs =
          case @scope
          when :to
            mail.to
          when :from, :sender
            mail.from
          when :cc
            mail.headers[:cc]
          when :bcc
            mail.headers[:bcc]
          when :subject
            mail.subject
          when :rcpt, :rcpts, :recipient, :recipients
            [mail.to, mail.headers[:cc], mail.headers[:bcc]].flatten.compact
          when :body
            mail.body
          when :tag, :tags, :in
            return @data.match_exact_string?(mail.tag_names)
            # has:seal, has:imprint, has:lock
          when :is
            case @data.str
            when "starred"
              return mail.starred?
            when "read"
              return mail.read?
            when "replied"
              return mail.replied?
              # sealed, imprinted, signed, locked, encrypted,
            else
              raise "NOT IMPLEMENTED: is:#{@data}"
            end
          when :before
            raise "NOT IMPLEMENTED"
          when :after
            raise "NOT IMPLEMENTED"
          when :att, :attachment
            raise "NOT IMPLEMENTED"
          else
            mail.headers[@scope] || (return false)
          end
        @data.match_string? strs
      end
    end
  end
end
