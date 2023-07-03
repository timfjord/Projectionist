BUILTIN_PROJECTIONS = {
    "mix.exs": {
        "mix.exs": {
            "alternate": "mix.lock",
        },
        "mix.lock": {
            "alternate": "mix.exs",
        },
    },
    "mix.exs&test/test_helper.exs": {  # Elixir mix with ExUnit
        "lib/*.ex": {
            "alternate": "test/{}_test.exs",
            "template": [
                "defmodule {camelcase|capitalize|dot} do",
                "end",
            ],
        },
        "test/*_test.exs": {
            "alternate": "lib/{}.ex",
            "template": [
                "defmodule {camelcase|capitalize|dot}Test do",
                "  use ExUnit.Case",
                "",
                "  alias {camelcase|capitalize|dot}",
                "end",
            ],
        },
    },
    "mix.exs&spec/spec_helper.exs": {  # Elixir mix with ESpec
        "lib/*.ex": {
            "alternate": "spec/{}_spec.exs",
            "template": [
                "defmodule {camelcase|capitalize|dot} do",
                "end",
            ],
        },
        "spec/*_spec.exs": {
            "alternate": "lib/{}.ex",
            "template": [
                "defmodule {camelcase|capitalize|dot}Spec do",
                "  use ESpec",
                "",
                "  alias {camelcase|capitalize|dot}",
                "end",
            ],
        },
    },
}
