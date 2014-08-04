require 'sinatra/base'
require 'sinatra/json'
require 'sinatra-index'
require 'json'
require 'net/http'

module PixelatedService
  class Server < Sinatra::Base
    set :root, File.join(File.dirname(__FILE__), '../../')
    set :public_folder, File.join(File.dirname(__FILE__), '../../../web-ui/app/')

    def json_body; JSON.parse request.body.read.to_s; end
    register Sinatra::Index
    use_static_index 'index.html'

    if ENV['RACK_ENV'] == 'staging'
      get    '/'            do File.read(File.join(settings.root, 'public', 'index.html')) end
    end

    get    '/mails'       do json mails(params["q"], (params["p"] || 0).to_i, (params["w"] || -1).to_i) end
    delete '/mails'       do json delete_mails(params["q"], (params["p"] || 0).to_i, (params["w"] || -1).to_i, params["idents"]) end
    post   '/mails/read'  do json readmails(params["idents"], true) end
    post   '/mails/unread'  do json readmails(params["idents"], false) end
    get    '/mail/:ident'    do |i| json mail(i)    end
    delete '/mail/:ident' do |i| json delete_mail(i) end
    post   '/mail/:ident/star'      do |i| json starmail(i, true)    end
    post   '/mail/:ident/unstar'    do |i| json starmail(i, false)    end
    post   '/mail/:ident/replied'      do |i| json repliedmail(i, true)    end
    post   '/mail/:ident/unreplied'    do |i| json repliedmail(i, false)    end
    post   '/mail/:ident/read'      do |i| json readmail(i, true)    end
    post   '/mail/:ident/unread'    do |i| json readmail(i, false)    end
    get    '/mail/:ident/tags'     do |i| json tags(i)    end
    post   '/mail/:ident/tags'    do |i| json settags(i, json_body)    end

    get    '/draft_reply_for/:ident' do |i| json draft_reply_for(i) end

    get    '/contacts'       do json contacts(params["q"], (params["p"] || 0).to_i, (params["w"] || -1).to_i) end
    get    '/contact/:ident'    do |i| json contact(i) end

    get    '/stats'       do json stats end

    get    '/personas'    do     json personas   end
    get    '/persona/:ident' do |i| json persona(i) end

    get    '/tags' do json all_tags(params["q"]) end

    post '/mails' do
      ident = send_mail json_body
      json({ ident: ident })
    end

    put '/mails' do
      ident = update_mail json_body
      json({ ident: ident })
    end

    post '/tags' do
      tag = create_tag json_body
      json({ tag: tag })
    end

    post '/control/create_mail'        do json control_create_mail  end
    post '/control/delete_mails'       do json control_delete_mails end
    post '/control/mailset/:name/load' do |name| json control_mailset_load(name) end


    # pass all other requests to asset server
    get '/*' do
      url = "http://localhost:9000/#{params['splat'][0]}"

      resp = Net::HTTP.get_response(URI.parse(url))
      if resp.is_a?(Net::HTTPSuccess)
        res = resp.body.to_s.gsub(/(href|src)=("|')\//, '\1=\2' + url + '/')
        content_type resp.content_type
        status resp.code
        res
      else
        status resp.code
        resp.message
      end
    end


    include PixelatedService::Fake
  end
end
