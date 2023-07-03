# taken from https://github.com/tpope/vim-rails/blob/master/autoload/rails.vim

BUILTIN_PROJECTIONS = {
    "Gemfile": {
        "Gemfile": {"alternate": "Gemfile.lock", "type": "lib"},
        "Gemfile.lock": {"alternate": "Gemfile"},
    },
    "script/about|config/application.rb": {  # Ruby on Rails
        "README": {"alternate": "config/database.yml"},
        "README.*": {"alternate": "config/database.yml"},
        "Rakefile": {"type": "task"},
        "app/channels/*_channel.rb": {
            "template": [
                "class {camelcase|capitalize|colons}Channel < ActionCable::Channel",
                "end",
            ],
            "type": "channel",
        },
        "app/controllers/*_controller.rb": {
            "template": [
                "class {camelcase|capitalize|colons}Controller < ApplicationController",
                "end",
            ],
            "type": "controller",
        },
        "app/controllers/concerns/*.rb": {
            "template": [
                "module {camelcase|capitalize|colons}",
                "\tinclude ActiveSupport::Concern",
                "end",
            ],
            "type": "controller",
        },
        "app/helpers/*_helper.rb": {
            "template": [
                "module {camelcase|capitalize|colons}Helper",
                "end",
            ],
            "type": "helper",
        },
        "app/jobs/*_job.rb": {
            "template": [
                "class {camelcase|capitalize|colons}Job < ActiveJob::Base",
                "end",
            ],
            "type": "job",
        },
        "app/mailers/*.rb": {
            "template": [
                "class {camelcase|capitalize|colons} < ActionMailer::Base",
                "end",
            ],
        },
        "app/models/*.rb": {
            "template": [
                "class {camelcase|capitalize|colons}",
                "end",
            ],
            "type": "model",
        },
        "app/serializers/*_serializer.rb": {
            "template": [
                "class {camelcase|capitalize|colons}Serializer < ActiveModel::Serializer",
                "end",
            ],
            "type": "serializer",
        },
        "config/*.yml": {
            "alternate": [
                "config/{}.example.yml",
                "config/{}.yml.example",
                "config/{}.yml.sample",
            ]
        },
        "config/*.example.yml": {"alternate": "config/{}.yml"},
        "config/*.yml.example": {"alternate": "config/{}.yml"},
        "config/*.yml.sample": {"alternate": "config/{}.yml"},
        "config/application.rb": {"alternate": "config/routes.rb"},
        "config/environment.rb": {"alternate": "config/routes.rb"},
        "config/environments/*.rb": {
            "alternate": ["config/application.rb", "config/environment.rb"],
            "type": "environment",
        },
        "config/initializers/*.rb": {"type": "initializer"},
        "config/routes.rb": {
            "alternate": ["config/application.rb", "config/environment.rb"],
            "type": "initializer",
        },
        "gems.locked": {"alternate": "gems.rb"},
        "gems.rb": {"alternate": "gems.locked", "type": "lib"},
        "lib/*.rb": {"type": "lib"},
        "lib/tasks/*.rake": {"type": "task"},
    },
    "script/about": {  # Ruby on Rails 2
        "config/environment.rb": {"type": "environment"}
    },
    "config/application.rb": {  # Ruby on Rails 3+
        "config/application.rb": {"type": "environment"}
    },
    "features/*.feature": {  # Cucumber
        "features/*.feature": {
            "template": ["Feature: {underscore|capitalize|blank}"],
            "type": "integration test",
        },
        "features/support/env.rb": {"type": "integration test"},
    },
    "spec/*_spec.rb": {  # RSpec
        "spec/*_spec.rb": {"alternate": "app/{}.rb"},
        "spec/controllers/*_spec.rb": {
            "template": [
                "require 'rails_helper'",
                "",
                "RSpec.describe {camelcase|capitalize|colons}, type: :controller do",
                "end",
            ],
            "type": "functional test",
        },
        "spec/features/*_spec.rb": {
            "template": [
                "require 'rails_helper'",
                "",
                'RSpec.describe "{underscore|capitalize|blank}", type: :feature do',
                "end",
            ],
            "type": "integration test",
        },
        "spec/helpers/*_spec.rb": {
            "template": [
                "require 'rails_helper'",
                "",
                "RSpec.describe {camelcase|capitalize|colons}, type: :helper do",
                "end",
            ],
            "type": "unit test",
        },
        "spec/integration/*_spec.rb": {
            "template": [
                "require 'rails_helper'",
                "",
                'RSpec.describe "{underscore|capitalize|blank}", type: :integration do',
                "end",
            ],
            "type": "integration test",
        },
        "spec/lib/*_spec.rb": {"alternate": "lib/{}.rb"},
        "spec/mailers/*_spec.rb": {
            "affinity": "controller",
            "template": [
                "require 'rails_helper'",
                "",
                "RSpec.describe {camelcase|capitalize|colons}, type: :mailer do",
                "end",
            ],
            "type": "functional test",
        },
        "spec/mailers/previews/*_preview.rb": {
            "affinity": "controller",
            "alternate": "app/mailers/{}.rb",
            "template": [
                "class {camelcase|capitalize|colons}Preview < ActionMailer::Preview",
                "end",
            ],
        },
        "spec/models/*_spec.rb": {
            "affinity": "model",
            "template": [
                "require 'rails_helper'",
                "",
                "RSpec.describe {camelcase|capitalize|colons}, type: :model do",
                "end",
            ],
            "type": "unit test",
        },
        "spec/rails_helper.rb": {"type": "integration test"},
        "spec/requests/*_spec.rb": {
            "template": [
                "require 'rails_helper'",
                "",
                'RSpec.describe "{underscore|capitalize|blank}", type: :request do',
                "end",
            ],
            "type": "integration test",
        },
        "spec/spec_helper.rb": {"type": "integration test"},
    },
    "test/*_test.rb": {  # MiniTest
        "test/*_test.rb": {"alternate": "app/{}.rb"},
        "test/controllers/*_test.rb": {
            "template": [
                "require 'test_helper'",
                "",
                "class {camelcase|capitalize|colons}Test < ActionController::TestCase",
                "end",
            ],
            "type": "functional test",
        },
        "test/functional/*_test.rb": {
            "alternate": ["app/controllers/{}.rb", "app/mailers/{}.rb"],
            "template": [
                "require 'test_helper'",
                "",
                "class {camelcase|capitalize|colons}Test < ActionController::TestCase",
                "end",
            ],
            "type": "functional test",
        },
        "test/helpers/*_test.rb": {
            "template": [
                "require 'test_helper'",
                "",
                "class {camelcase|capitalize|colons}Test < ActionView::TestCase",
                "end",
            ],
            "type": "unit test",
        },
        "test/integration/*_test.rb": {
            "template": [
                "require 'test_helper'",
                "",
                "class {camelcase|capitalize|colons}Test < ActionDispatch::IntegrationTest",
                "end",
            ],
            "type": "integration test",
        },
        "test/lib/*_test.rb": {"alternate": "lib/{}.rb"},
        "test/mailers/*_test.rb": {
            "affinity": "model",
            "template": [
                "require 'test_helper'",
                "",
                "class {camelcase|capitalize|colons}Test < ActionMailer::TestCase",
                "end",
            ],
            "type": "functional test",
        },
        "test/mailers/previews/*_preview.rb": {
            "affinity": "controller",
            "alternate": "app/mailers/{}.rb",
            "template": [
                "class {camelcase|capitalize|colons}Preview < ActionMailer::Preview",
                "end",
            ],
        },
        "test/models/*_test.rb": {
            "affinity": "model",
            "template": [
                "require 'test_helper'",
                "",
                "class {camelcase|capitalize|colons}Test < ActiveSupport::TestCase",
                "end",
            ],
            "type": "unit test",
        },
        "test/jobs/*_test.rb": {
            "affinity": "job",
            "template": [
                "require 'test_helper'",
                "",
                "class {camelcase|capitalize|colons}Test < ActiveJob::TestCase",
                "end",
            ],
            "type": "unit test",
        },
        "test/test_helper.rb": {"type": "integration test"},
        "test/unit/*_test.rb": {
            "affinity": "model",
            "alternate": ["app/models/{}.rb", "lib/{}.rb"],
            "template": [
                "require 'test_helper'",
                "",
                "class {camelcase|capitalize|colons}Test < ActiveSupport::TestCase",
                "end",
            ],
            "type": "unit test",
        },
        "test/unit/helpers/*_helper_test.rb": {
            "affinity": "controller",
            "alternate": "app/helpers/{}_helper.rb",
        },
    },
    "spec/acceptance/*.feature": {  # Turnip
        "spec/acceptance/*.feature": {
            "template": ["Feature: {underscore|capitalize|blank}"],
            "type": "integration test",
        }
    },
}
