# Syntax notes for search:
#   you can put a - in front of any search term to negate it
#   you can scope a search by putting a name of a scope, a colon and then the search term WITHOUT a space.
#     scoping will allow you to search for more things than otherwise available
#     an unknown scope name will be assumed to be a header to search
#   you can surround a search term in quotes to search for the whole thing
#   multiple search terms will be ANDed together
#   you can OR things by using the keyword OR/or - if you have it without parens, you will or the whole left with the whole right, until we find another or.
#      if you use parenthesis, you can group together terms
#   search in:_default_, in:all, in:trash, in:sent, in:drafts will only work for the WHOLE search. You can do a negation on a scoped search if it's in:trash, in:sent or in:drafts, but not for in:all

module Smail
  class Search
    def initialize(q)
      if q
        @qtree, @search_scope = Search.compile(q)
      else
        @qtree, @search_scope = TrueMatch.new, Smail::MailScopeFilter::Default
      end
    end

    def restrict(input)
      @search_scope.new(input).select do |mm|
        @qtree.match?(mm)
      end
    end

    REGEXP_DQUOTED = /"[^"]*"/
    REGEXP_SQUOTED = /'[^']*'/
    REGEXP_SCOPE = /\w+:(".*?"|'.*?'|[^\s\)]+)/
    REGEXP_OTHER = /[^\s\)]+/

    def self.scan_literal(qs)
      if qs.check(REGEXP_DQUOTED)
        StringMatch.new(qs.scan(REGEXP_DQUOTED), true)
      elsif qs.check(REGEXP_SQUOTED)
        StringMatch.new(qs.scan(REGEXP_SQUOTED), true)
      elsif qs.check(REGEXP_OTHER)
        StringMatch.new(qs.scan(REGEXP_OTHER))
      end
    end

    def self.combine_search_scopes(l, r)
      l + r
    end

    def self.compile(q, qs = StringScanner.new(q))
      qtree = AndMatch.new
      search_scope = Smail::MailScopeFilter::Default
      until qs.eos?
        if qs.check(/\)/)
          qs.scan(/\)/)
          return optimized(qtree), search_scope
        end

        negated = false
        if qs.check(/-/)
          negated = true
          qs.scan(/-/)
        end

        if qs.check(/or/i)
          qs.scan(/or/i)
          left = qtree
          qtree = OrMatch.new(left, AndMatch.new)
        else
          res =
            if qs.check(/\(/)
              qs.scan(/\(/)
              v, sc = compile(q, qs)
              search_scope = search_scope + sc
              v
            elsif qs.check(REGEXP_DQUOTED)
              StringMatch.new(qs.scan(REGEXP_DQUOTED), true)
            elsif qs.check(REGEXP_SQUOTED)
              StringMatch.new(qs.scan(REGEXP_SQUOTED), true)
            elsif qs.check(REGEXP_SCOPE)
              scope = qs.scan(/\w+/)
              qs.scan(/:/)
              rest_node = scan_literal(qs)
              v = ScopeMatch.new(scope, rest_node)
              if v.is_search_scope? && !negated
                search_scope = search_scope + v.search_scope
                TrueMatch.new
              else
                v
              end
            elsif qs.check(REGEXP_OTHER)
              StringMatch.new(qs.scan(REGEXP_OTHER))
            end
          res = NegateMatch.new(res) if negated
          qtree << res
        end

        qs.scan(/\s+/)
      end
      return optimized(qtree), search_scope
    end

    def self.optimized(tree)
      case tree
      when AndMatch
        data = tree.data.reject { |d| TrueMatch === d }
        if data.length == 1
          optimized(data.first)
        else
          AndMatch.new(data.map { |n| optimized(n)} )
        end
      when OrMatch
        if tree.right.is_a?(AndMatch) && tree.right.data.empty?
          optimized(tree.left)
        else
          OrMatch.new(optimized(tree.left), optimized(tree.right))
        end
      when NegateMatch
        if tree.data.is_a?(NegateMatch)
          optimized(tree.data.data)
        else
          NegateMatch.new(optimized(tree.data))
        end
      else
        tree
      end
    end
  end
end

require 'smail/search/string_match'
require 'smail/search/scope_match'
require 'smail/search/negate_match'
require 'smail/search/and_match'
require 'smail/search/or_match'
require 'smail/search/true_match'
