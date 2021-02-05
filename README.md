# Twitter-Threader-Bot
<h2>Table of Contents</h2>
    <ul>
        <li><a href="#about">About</a></li>
        <li>
        <a href="#class-methods">Class Methods</a>
            <ul>
                <li>
                    <a href="#method-userThread">userThread</a>
                </li>
                <li>
                    <a href="#method-Tweet">Tweet</a>
                </li>
                <li>
                    <a href="#method-ThreadCompiler">ThreadCompiler</a>
                </li>
                <li>
                    <a href="#method-FirebaseUtility">FirebaseUtility</a>
                </li>
                <li>
                    <a href="#method-ThreaderBot">ThreaderBot</a>
                </li>
            </ul>
        </li>
        <li><a href="#surfing-method">surfBot(args)</a></li>
        <li><a href="#responseGen-method">responseGen(args)</a></li>
        <li><a href="https://sobydamn.github.io/TwitterThread/#how-to-box">How to use?</a></li>
    </ul>
<hr>
<h2 id="about">About</h2>
    <p>
    Twitter has many great people sharing valuable information in the form of threads.
    This is a twitter bot which can be used to compile threads and view it at one place or share it with others, this can also be used to print the thread and save it as pdf format for later consumption.
    </p>
<h2><strong><a name="method-userThread">userThread(id, name,username,profile_img,tweets)</a></strong></h2>
    <p>
        Creates a userThread object containing details about user and the thread together.
    </p>
    <dl>
        <dt><h3>Arguments:</h3></dt>
        <dd>
            <p>
                id - profile id of thread owner
                <br>
                name - name of the thread owner
                <br>
                username - username of the thread owner
                <br>
                profile_img - link to the profile image of thread owner
                <br>
                tweets - Array of tweets in the thread
            </p>
        </dd>
        <dt><h3>Attributes:</h3></dt>
        <dd>
            <p>
                id - profile id of thread owner
                <br>
                name - name of the thread owner
                <br>
                username - username of the thread owner
                <br>
                profile_img - link to the profile image of thread owner
                <br>
                tweets - Array of tweets in the thread
                <br>
            </p>
        </dd>
        <dt><h3>Methods:</h3></dt>
        <dl>
            <dt><h4>to_dict()</h4></dt>
            <dd>return dictionary of all the Attributes</dd>
        </dl>
    </dl>
<h2><strong><a name="method-Tweet">Tweet(text,date,medias,tweet_id,urls)</a></strong></h2>
    Creates a tweet object to store details of a tweet.
    <dl>
        <dt><h3>Arguments:</h3></dt>
        <dd>
            <p>
                text - full text of the tweet
                <br>
                date - date of the tweet
                <br>
                medias - array of dictionary of media with values:
                <br>
                tweet_id - tweet's unique id
                <br>
                urls - Array of url included in tweet
                <br>
            </p>
        </dd>
        <dt><h3>Attributes:</h3></dt>
        <dd>
            <p>
                text - full text of the tweet
                <br>
                date - date of the tweet
                <br>
                medias - array of dictionary of media with values:
                <ul>
                    <li>
                        type - video/photo
                    </li>
                    <li>
                        media_url_https - url of media file https(shorten)
                    </li>
                    <li>
                        media_url - url of media file(shorten)
                    </li>
                    <li>
                        expanded_url - expanded url 
                    </li>
                </ul>
                <br>
                tweet_id - tweet's unique id
                <br>
                urls - Array of url included in tweet
                <br>
            </p>
        </dd>
        <dt><h3>Methods:</h3></dt>
        <dl>
            <dt>
                <h4>to_dict()</h4>
            </dt>
            <dd>
                return dictionary of all the Attributes
            </dd>
        </dl>
    </dl>
<h2><strong><a name="method-ThreadCompiler">ThreadCompiler(tweet_id,user_id,thread_request_id,easy_compile=True,max_tweets_to_look=5000)</a></strong></h2>
    <dl>
        <dt><h3>Arguments:</h3></dt>
        <dd>
            tweet_id - id of the tweet under which request was method-ThreaderBot
            <br>
            user_id - twitter id of the thread owner
            <br>
            thread_request_id - id of the user's tweet who requested thread compile
            <br>
            easy_compile - rolling up to the parent (use when thread is too old)
            <br>
            max_tweets_to_look - max tweets you want to look for to reach to the thread
        </dd>
        <dt><h3>Attributes:</h3></dt>
        <dd>
            id - id of the parent tweet_id
            <br>
            tweets - Array of <a href="#method-Tweet">Tweet</a> object
            <br>
            tweet_id - id of the tweet under which request was made.
            <br>
            user_id - twitter id of the thread owner
            <br>
            thread_request_id - id of the user's tweet who requested thread compile
            <br>
            easy_compile - rolling up to the parent (use when thread is too old)
            <br>
            max_tweets_to_look - max tweets you want to look for to reach to the thread
        </dd>
        <dt><h3>Methods:</h3></dt>
        <dd>
            <dl>
                <dt><h4>compileTweets()</h4></dt>
                <dd>
                    returns array of <a href="#method-Tweet">Tweet</a> object
                </dd>
                <dt><h4>tweetCompilerBottom(since_id=None)</h4></dt>
                <dd>compiles the bottom tweet till since_id and returns array of <a href="#method-Tweet">Tweet</a> object <i>(all tweets including upper part)</i></dd>
                <dd>
                    <dl>
                        <dt>args:</dt>
                        <dd>
                            since_id - id of the tweet till which compiling is needed
                        </dd>
                    </dl>
                </dd>
                <dt>fetchBottomThread(tweets_track,tweet_id=None)</dt>
                <dd>returns the array of <a href="#method-Tweet">Tweet</a> object possibly the longest thread till the <i>tweet_id</i></dd>
                <dd>
                    <dl>
                        <dt>args:</dt>
                        <dd>
                            tweets_track - contains all the tweets as dictionary with key as tweet id and elements <i>tweet</i> containing <a href="#method-Tweet">Tweet</a> object and <i>in_reply_to_status_id</i> till tweet_id from threads owner profile.
                            <br>
                            tweet_id - id of the tweet under which request was made.
                        </dd>
                    </dl>
                </dd>
                <dt><h4>compileThread()</h4></dt>
                <dd>returns <a href="#method-userThread">userThread</a> object</dd>
                <dt><h4>save(threadData)</h4></dt>
                <dd>
                    Saves threadData to database.
                </dd>
                <dd>
                    <dl>
                        <dt>args:</dt>
                        <dd>
                            threaData - dictionary returned by <i>to_dict</i> method of <a href="#method-userThread">userThread</a> class.
                        </dd>
                    </dl>
                </dd>
                <dt><h4>getThreadID()</h4></dt>
                <dd>
                    returns id of parent tweet of the thread as string
                </dd>
            </dl>
        </dd>
    </dl>
<h2><strong><a name="method-FirebaseUtility">FirebaseUtility(cred)</a></strong></h2>
    <dl>
        <dt><h3>Arguments:</h3></dt>
        <dd>
            <p>
                cred - google firebase firestore credentials
            </p>
        </dd>
        <dt><h3>Attributes:</h3></dt>
        <dd>
            <p>
                cred - contains google firebase firestore credentials
                <br>
                db - Database firestore client
            </p>
        </dd>
        <dt><h3>Methods:</h3></dt>
        <dd>
            <dl>
                <p>
                    <dt>
                        <h4>
                            initialize()
                        </h4>
                    </dt>
                    <dd>
                        <p>
                            initialize the firebase app through the given credentials
                        </p>
                    </dd>
                    <dt>
                        <h4>
                            documentExists(thread_id:"Thread parent id",thread_len:"Length of fetched thread")
                        </h4>
                    </dt>
                    <dd>
                        <p>
                            Returns true when document with given thread_id exists in database and has length greater than thread_len
                        </p>
                    </dd>
                    <dd>
                        <dl>
                            <dt>
                                <h5>
                                    Args:
                                </h5>
                            </dt>
                            <dd>
                                <p>
                                    thread_id - id of the parent tweet of the thread
                                    <br>
                                    thread_len - length of the thread
                                </p>
                            </dd>
                        </dl>
                    </dd>
                    <dt>
                        <h4>
                            storeData(thread_id,data:"dictionary")
                        </h4>
                    </dt>
                    <dd>
                        <p>
                            stores the thread data in database with given thread id if it doesn't exist before or data has length greater than stored thread length
                        </p>
                    </dd>
                    <dd>
                        <dl>
                            <dt>
                                <h5>
                                    Args:
                                </h5>
                            </dt>
                            <dd>
                                <p>
                                    thread_id - id of the parent tweet of the thread
                                    <br>
                                    data - dictionary containing parameters returned by <i>to_dict()</i> of <a href="#method-userThread">userThread</a> class.
                                </p>
                            </dd>
                        </dl>
                    </dd>
                </p>
            </dl>
        </dd>
    </dl>
<h2><strong><a name="method-ThreaderBot">ThreaderBot(file_name="since_id.txt")</a></strong></h2>
    <dl>
        <dt><h3>Arguments:</h3></dt>
        <dd>
            <p>
                file_name - name of the file to store the <i>since_id</i>
            </p>
        </dd>
        <dt><h3>Attributes:</h3></dt>
        <dd>
            <p>
                since_id = the id of the last request tweet
            </p>
        </dd>
        <dt><h3>Methods:</h3></dt>
        <dd>
            <dl>
                <dt>
                    <h4>
                        retrieve_since_id(file_name="since_id.txt")
                    </h4>
                </dt>
                <dd>
                    <p>
                        returns the since_id stored in the file
                    </p>
                </dd>
                <dd>
                    <dl>
                        <dt>args:</dt>
                        <dd>
                            file_name - name of the file where <i>since_id</i> is stored
                        </dd>
                    </dl>
                </dd>
                <dt><h4>store_since_id(since_id, file_name="since_id.txt")</h4></dt>
                <dd>
                    <p>
                        Stores the since_id in given file_name
                    </p>
                </dd>
                <dd>
                    <dl>
                        <dt>args:</dt>
                        <dd>
                            file_name - name of the file where <i>since_id</i> is stored<br>
                            since_id - the id of the last request tweet
                        </dd>
                    </dl>
                </dd>
                <dt><h4>fetchTweets()</h4></dt>
                <dd>
                    Fetches the tweet in timeline and looks for mentions of own id till the <i>since_id</i> i.e the last mention and returns the array of all mentions<br>
                    <i>Note:-Retweet will trigger this aswell</i>
                </dd>
                <dt><h4>run()</h4></dt>
                <dd>
                    returns false if <i>fetchTweets()</i> method returns empty array else return array of requests as tuples if it's a reply under a tweet with text containing <b>compile</b> or <b>ezcompile</b>
                    <br>
                    tuple - 
                    <i>(in_reply_to_status_id,in_reply_to_user_id,screen_name,id,easy_compile)</i>
                    <dl>
                        <dt>Returned tuple elements</dt>
                        <dd>
                            in_reply_to_status_id - id of the tweet which user has mentioned us.
                            <br>
                            in_reply_to_user_id - user id of the tweet which user has mentioned us.
                            <br>
                            screen_name - username of the twitter id who has sent the compile request(used to respond)
                            <br>
                            id - id of the request tweet
                            <br>
                            easy_compile - whether the compile method is ezcompile or not (bool)
                        </dd>
                    </dl>
                </dd>
                <dt><h4>sendResponse(text,request_username,rquest_id)</h4></dt>
                <dd>
                    sends response/reply to request tweet
                </dd>
                <dd>
                    <dl>
                        <dt>args:</dt>
                        <dd>
                            text - string containing response text
                            <br>
                            request_username - username of the request tweet
                            <br>
                            rquest_id - id of the request tweet
                            <br>
                            <b><i>Note: read and write permissions are required from twitter api project</i></b>
                        </dd>
                    </dl>
                </dd>
                <dt><h4>sendResponseDirectMessage(self,text,id)</h4></dt>
                <dd>
                    sends response as direct message.
                </dd>
                <dd>
                    <dl>
                        <dt>args:</dt>
                        <dd>
                            text - string containing response text
                            <br>
                            id - user id
                            <br>
                            <b><i>Note: read and write permissions are required from twitter api project</i></b>
                        </dd>
                    </dl>
                </dd>
            </dl>
        </dd>
    </dl>
<dl>
    <dt><h2><strong><a name="surfing-method">surfBot(bot:"ThreadBot")</a></strong></h2></dt>
    <dd>
        compiles the tweet and save it to the database then send respond with id of parent tweet
    </dd>
    <dt><h3>Arguments:</h3></dt>
    <dd>
        bot - <a href="#method-ThreaderBot">ThreaderBot</a> object.
    </dd>
</dl>
<dl>
    <dt><h2><strong><a name="responseGen-method">responseGen(link,tweetText,thread_len)</a></strong></h2></dt>
    <dd>
        returns random response text
    </dd>
    <dt><h3>Arguments:</h3></dt>
    <dd>
        link - link of the Thread
        <br>
        tweetText - text of a tweet to be included with response text
        <br>
        thread_len - length of the thread
    </dd>
</dl>