

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
LOGIN_PAGE_HTML = """\
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="/css/bootstrap.css" rel="stylesheet" />
        </head>
        <body>
        <div class="container">
            <br/>
            <br/>
            <a class="btn" data-toggle="modal" href="#myModal" role="button">Students &raquo;</a></p>
        <div aria-hidden="true" aria-labelledby="myModalLabel" class="modal hide fade" id="myModal" role="dialog" tabindex="-1">
           <div class="modal-header">
            <button aria-hidden="true" class="close" data-dismiss="modal" type="button">x</button>
            <h3 id="myModalLabel">
             Student Login</h3>
           </div>
           <div class="modal-body">
                        %s
           </div>
            <div class="modal-footer">
                <button class="btn" data-dismiss="modal">Close</button></div>
            </div>
         </div>
         </div>
                        <script src="/js/bootstrap.js"></script>
                        <script src="/js/jquery.js"></script>
                        <script src="/js/bootstrap.min.js"></script>
                        </body>
                        </html>
    """