# app.rb
require 'rails'
require 'active_record'
require 'action_controller/railtie'
require 'pg'

puts "=" * 60
puts "PG Admin - Database Management Tool"
puts "=" * 60
puts "Starting with:"
puts "  Ruby: #{RUBY_VERSION}"
puts "  Rails: #{Rails.version}"
puts "  Passenger: #{`passenger --version | head -1`.strip}"
puts "=" * 60

# Конфигурация Rails приложения
module PGAdmin
  class Application < Rails::Application
    config.load_defaults 7.0
    config.secret_key_base = 'pgadmin-secret-key-for-development'
    config.eager_load = false
    config.hosts << "localhost"
    config.hosts << "app"
    config.logger = Logger.new(STDOUT)
    config.log_level = :info
  end
end

# Инициализация приложения
PGAdmin::Application.initialize!

# Подключение к PostgreSQL
begin
  db_url = ENV['DATABASE_URL'] || 'postgresql://pgadmin:password@postgres:5432/pgadmin_db'
  ActiveRecord::Base.establish_connection(db_url)
  ActiveRecord::Base.connection.execute("SELECT 1")
  puts "✅ Connected to PostgreSQL successfully"
rescue => e
  puts "⚠️ Could not connect to PostgreSQL: #{e.message}"
end

# Главный контроллер
class DatabaseController < ActionController::Base
  skip_forgery_protection  
  layout false
  
  # Главная страница - список всех баз данных
  def index
    @databases = ActiveRecord::Base.connection.execute(
      "SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname"
    )
    render html: index_html.html_safe
  end
  
  # Просмотр таблиц в выбранной базе
  def show_database
    @database = params[:database]
    
    # Переключаемся на выбранную базу
    switch_connection(@database)
    
    @tables = ActiveRecord::Base.connection.execute(
      "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename"
    )
    
    render html: database_html.html_safe
  end
  
  # Просмотр содержимого таблицы
  def show_table
    @database = params[:database]
    @table = params[:table]
    
    switch_connection(@database)
    
    @columns = ActiveRecord::Base.connection.columns(@table)
    @rows = ActiveRecord::Base.connection.execute("SELECT * FROM #{@table} LIMIT 100")
    
    render html: table_html.html_safe
  end
  
  # Выполнение SQL запроса
  def query
    @database = params[:database]
    @query = params[:query]
    
    if @query.present?
      switch_connection(@database)
      begin
        @result = ActiveRecord::Base.connection.execute(@query)
        @message = "Query executed successfully"
      rescue => e
        @error = e.message
      end
    end
    
    render html: query_html.html_safe
  end
  
  private
  
  def switch_connection(database)
    db_url = ENV['DATABASE_URL'].gsub(/\/[^\/]+$/, "/#{database}")
    ActiveRecord::Base.establish_connection(db_url)
  end
  
  def index_html
    <<-HTML
    <!DOCTYPE html>
    <html>
    <head>
        <title>PG Admin - Databases</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; }
            .navbar { background: #2c3e50; color: white; padding: 1rem 2rem; }
            .container { max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
            .card { background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); padding: 1.5rem; margin-bottom: 1.5rem; }
            h1 { font-size: 1.8rem; margin-bottom: 1rem; }
            h2 { font-size: 1.4rem; margin-bottom: 1rem; color: #2c3e50; }
            .db-list { list-style: none; }
            .db-item { padding: 1rem; border-bottom: 1px solid #eee; display: flex; align-items: center; }
            .db-item:hover { background: #f8f9fa; }
            .db-icon { font-size: 1.5rem; margin-right: 1rem; }
            .db-name { font-size: 1.1rem; font-weight: 500; color: #2c3e50; text-decoration: none; }
            .db-name:hover { text-decoration: underline; }
            .badge { background: #e9ecef; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; margin-left: 1rem; }
            .btn { display: inline-block; padding: 0.5rem 1rem; background: #3498db; color: white; text-decoration: none; border-radius: 4px; font-size: 0.9rem; }
            .btn:hover { background: #2980b9; }
            table { width: 100%; border-collapse: collapse; }
            th { background: #f8f9fa; padding: 0.75rem; text-align: left; font-weight: 600; }
            td { padding: 0.75rem; border-bottom: 1px solid #dee2e6; }
            tr:hover { background: #f8f9fa; }
            textarea { width: 100%; min-height: 150px; font-family: monospace; padding: 0.5rem; border: 1px solid #dee2e6; border-radius: 4px; }
            .alert { padding: 1rem; border-radius: 4px; margin-bottom: 1rem; }
            .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
            .alert-danger { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        </style>
    </head>
    <body>
        <div class="navbar">
            <h1 style="font-size: 1.5rem; margin:0;">🐘 PG Admin - Database Manager</h1>
        </div>
        <div class="container">
            <div class="card">
                <h2>📊 Databases</h2>
                <p>Process ID: #{Process.pid} | Passenger: #{`passenger --version | head -1`.strip}</p>
            </div>
            <div class="card">
                <ul class="db-list">
                #{@databases.map do |db|
                    "<li class='db-item'>
                        <span class='db-icon'>📁</span>
                        <a href='/databases/#{db['datname']}' class='db-name'>#{db['datname']}</a>
                        <span class='badge'>PostgreSQL</span>
                    </li>"
                end.join}
                </ul>
            </div>
        </div>
    </body>
    </html>
    HTML
  end
  
  def database_html
    <<-HTML
    <!DOCTYPE html>
    <html>
    <head>
        <title>PG Admin - #{@database}</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; }
            .navbar { background: #2c3e50; color: white; padding: 1rem 2rem; }
            .container { max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
            .card { background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); padding: 1.5rem; margin-bottom: 1.5rem; }
            .nav-links { margin-bottom: 1rem; }
            .nav-links a { color: white; text-decoration: none; margin-right: 1rem; }
            .nav-links a:hover { text-decoration: underline; }
            .btn { display: inline-block; padding: 0.5rem 1rem; background: #3498db; color: white; text-decoration: none; border-radius: 4px; font-size: 0.9rem; margin-right: 0.5rem; }
            .btn:hover { background: #2980b9; }
            .btn-success { background: #28a745; }
            .btn-success:hover { background: #218838; }
        </style>
    </head>
    <body>
        <div class="navbar">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h1 style="font-size: 1.5rem;">📁 Database: #{@database}</h1>
                <div class="nav-links">
                    <a href='/'>← Back to Databases</a>
                    <a href='/databases/#{@database}/query'>🔍 New Query</a>
                </div>
            </div>
        </div>
        <div class="container">
            <div class="card">
                <h2>📋 Tables</h2>
                <div style="margin-top: 1rem;">
                #{@tables.map do |t|
                    "<div style='margin-bottom: 0.5rem;'>
                        <a href='/databases/#{@database}/tables/#{t['tablename']}' style='text-decoration: none; color: #3498db;'>
                            📊 #{t['tablename']}
                        </a>
                    </div>"
                end.join}
                </div>
            </div>
        </div>
    </body>
    </html>
    HTML
  end
  
  def table_html
    <<-HTML
    <!DOCTYPE html>
    <html>
    <head>
        <title>PG Admin - #{@table}</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; }
            .navbar { background: #2c3e50; color: white; padding: 1rem 2rem; }
            .container { max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
            .card { background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); padding: 1.5rem; margin-bottom: 1.5rem; overflow-x: auto; }
            table { width: 100%; border-collapse: collapse; }
            th { background: #f8f9fa; padding: 0.75rem; text-align: left; font-weight: 600; border-bottom: 2px solid #dee2e6; }
            td { padding: 0.75rem; border-bottom: 1px solid #dee2e6; font-family: monospace; }
            tr:hover { background: #f8f9fa; }
        </style>
    </head>
    <body>
        <div class="navbar">
            <h1>📊 Table: #{@table}</h1>
            <a href='/databases/#{@database}' style='color: white;'>← Back to tables</a>
        </div>
        <div class="container">
            <div class="card">
                <table>
                    <thead>
                        <tr>
                            #{@columns.map { |c| "<th>#{c.name}</th>" }.join}
                        </tr>
                    </thead>
                    <tbody>
                        #{@rows.map do |row|
                            "<tr>#{@columns.map { |c| "<td>#{row[c.name.to_s]}</td>" }.join}</tr>"
                        end.join}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    HTML
  end
  
  def query_html
    <<-HTML
    <!DOCTYPE html>
    <html>
    <head>
        <title>PG Admin - Query</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; }
            .navbar { background: #2c3e50; color: white; padding: 1rem 2rem; }
            .container { max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
            .card { background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); padding: 1.5rem; margin-bottom: 1.5rem; overflow-x: auto; }
            textarea { width: 100%; min-height: 150px; font-family: monospace; padding: 0.5rem; border: 1px solid #dee2e6; border-radius: 4px; margin-bottom: 1rem; }
            .btn { padding: 0.5rem 1rem; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
            .btn:hover { background: #2980b9; }
            .alert { padding: 1rem; border-radius: 4px; margin-bottom: 1rem; }
            .alert-success { background: #d4edda; color: #155724; }
            .alert-danger { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <div class="navbar">
            <h1>🔍 SQL Query - #{@database}</h1>
            <a href='/databases/#{@database}' style='color: white;'>← Back to database</a>
        </div>
        <div class="container">
            <div class="card">
                <form method='post' action='/databases/#{@database}/query'>
                    <textarea name='query'>#{@query}</textarea>
                    <button type='submit' class='btn'>Execute Query</button>
                </form>
            </div>
            
            #{if @message
                "<div class='alert alert-success'>#{@message}</div>"
            elsif @error
                "<div class='alert alert-danger'>#{@error}</div>"
            end}
            
            #{if @result && @result.ntuples > 0
                "<div class='card'>
                    <table>
                        <thead>
                            <tr>#{@result.fields.map { |f| "<th>#{f}</th>" }.join}</tr>
                        </thead>
                        <tbody>
                            #{@result.map do |row|
                                "<tr>#{row.values.map { |v| "<td>#{v}</td>" }.join}</tr>"
                            end.join}
                        </tbody>
                    </table>
                </div>"
            elsif @result
                "<div class='card'>Query executed. #{@result.cmd_tuples} rows affected.</div>"
            end}
        </div>
    </body>
    </html>
    HTML
  end
end

# Маршруты
PGAdmin::Application.routes.draw do
  root 'database#index'
  
  get '/databases/:database', to: 'database#show_database'
  get '/databases/:database/tables/:table', to: 'database#show_table'
  get '/databases/:database/query', to: 'database#query'
  post '/databases/:database/query', to: 'database#query'
end

# Запуск
Rack::Builder.new.run PGAdmin::Application