# config.ru
require_relative 'app'

# Логирование запросов
class RequestLogger
  def initialize(app)
    @app = app
  end

  def call(env)
    puts "[#{Time.now.strftime('%H:%M:%S')}] #{env['REQUEST_METHOD']} #{env['PATH_INFO']} (PID: #{Process.pid})"
    @app.call(env)
  end
end

use RequestLogger
run PGAdmin::Application