# Twitter-Threader-Bot
<h2>Table of Contents</h2>
    <ul>
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
        <li><a href="#about">About</a></li>
        <li><a href="#how-to-use">How to use?</a></li>
    </ul>
<hr>
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
    <h3>Attributes:</h3>
    <p>
    </p>
    <h3>Methods:</h3>
    <p>

    </p>
    <p>

    </p>
    <h3>Arguments:</h3>
    <p>
    </p>
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
    <h3>Arguments:</h3>
    <dd>
        <p>
            file_name - name of the file to store the <i>since_id</i>
        </p>
    </dd>
    <h3>Attributes:</h3>
    <dd>
        <p>
            since_id = stores the id of the last request tweet
        </p>
    </dd>
    <h3>Methods:</h3>
    <dd>
        <h4>
            retrieve_since_id(file_name="since_id.txt")
        </h4>
        <p>
            returns the since_id stored in the file
        </p>
    </dd>
<h2 id="about">About</h2>
<p>Twitter has many great people sharing valuable information in the form of threads.
This is a twitter bot which can be used to compile threads and view it at one place or share it with others, this can also be used to print the thread and save it as pdf format for later consumption.</p>
<h2 id="how-to-use">How to use?</h2>
<p><i>Currently there are two methods in which a thread can be compiled for you to view.</i></p>
<b>#Method1</b>
<ol>
<li>Go to the twitter thread which you want to compile.</li>
<li>
<p>
    At any part of the thread reply with <b><a href="https://twitter.com/ThreaderTweet" style="text-decoration: none;">@ThreaderTweet</a> compile</b>.
    <br>
    The bot will soon reply to you with to a link of compiled thread.
</p>
</li>
</ol>
<div>
    <img src="https://sobydamn.github.io/TwitterThread/bot_using_compile_arg.png"/>
</div>
<p id="#how-to-method2">#Method 2</p>
<ol>
    <li>
        <p>Go to the <b>bottom</b> of the thread i.e the last tweet of the thread.</p>
    </li>
    <li>
        <p>
            At the extreme bottom of the thread reply with <b><a href="https://twitter.com/ThreaderTweet" style="text-decoration: none;">@ThreaderTweet </a>ezcompile</b>.
            <br>
            The bot will soon reply to you with to a link of compiled thread.
        </p>
    </li>
</ol>
<div class="how-to-img-holder">
    <img src="https://sobydamn.github.io/TwitterThread/bot_use_ezcompile.png"/>
</div>