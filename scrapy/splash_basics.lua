function main(splash, args)
    -- Open the URL
    url = args.url
    assert(splash:go(url))
    -- Wait for the page to fully load
    assert(splash:wait(0.5))

    return {
        html = splash:html(),
        png = splash:png(),
    }


end