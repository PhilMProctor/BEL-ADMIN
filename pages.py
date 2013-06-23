

sADMIN_PAGE_HTML = """\
    <!DOCTYPE html>
    <html>
    <body>
      <form action="" method="post">
      <label for="username">username</label>:
      <input type="text" name="username" id="username" />
      <br/>
      <label for="password">password</label>:
      <input type="text" name="password" id="password" />
      <br/>
      <label for="courseN">course number</label>:
      <input type="text" name="courseN" id="courseN" />
      <br/>
      <label for="courseT">course type</label>:
      <input type="text" name="courseT" id="courseT" />
      <br/>
      <input type="submit" value=submit />                 
      </form>
    </body>
    </html>
    """ 
WELCOME = """\
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="/css/bootstrap.css" rel="stylesheet" />
        </head>
        <body>
        <div class="container">
           Welcome so happy to see you %s 
        </div>
                        <script src="/js/bootstrap.js"></script>
                        <script src="/js/jquery.js"></script>
                        <script src="/js/bootstrap.min.js"></script>
                        </body>
                        </html>
    """