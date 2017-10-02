import math

def boolean(value, summary,  posts_with_word=0, total_posts=1):
    return 1.0 if (value > 0.0) else 0.0


def tf(value, summary,  posts_with_word=0, total_posts=1):
    return float(value) / float(summary)


def idf(value, summary,  posts_with_word=0, total_posts=1):
    idf_value = 0.0
    if posts_with_word > 0:
        idf_value = math.log(float(total_posts) / float(posts_with_word))
    return idf_value


def tf_idf(value, summary, posts_with_word=0, total_posts=1):
    return tf (value, summary, posts_with_word, total_posts) * \
           idf(value, summary, posts_with_word, total_posts)


def log_tf(value, summary, posts_with_word=0, total_posts=1):
    log_value = 0.0
    if value > 0.0:
       log_value = math.log(tf(value, summary, posts_with_word, total_posts), 2)
    return log_value

SCHEMES = {
      'boolean' : boolean
    , 'tf'      : tf
    , 'idf'     : idf
    , 'tf_idf'  : tf_idf
    , 'log_tf'  : log_tf
}
