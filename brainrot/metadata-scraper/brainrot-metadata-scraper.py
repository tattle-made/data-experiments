import marimo

__generated_with = "0.19.4"
app = marimo.App()


@app.cell
def _():
    import instaloader
    from instaloader import Post, PostComment, Profile, InstaloaderContext
    import os
    from sqlmodel import SQLModel
    from datetime import datetime, timezone
    from itertools import islice
    return InstaloaderContext, Post, SQLModel, datetime, instaloader, os


@app.cell
def _(instaloader, os):
    def configure_instaloader():
        ig = instaloader.Instaloader()

        username = os.getenv("INSTAGRAM_USERNAME")
        password = os.getenv("INSTAGRAM_PASSWORD")
    
        ig.login(username, password)
        return ig

    ig_loader = configure_instaloader()
    return (ig_loader,)


@app.cell
def _(SQLModel, datetime):
    class BrainrotPostEngagement(SQLModel):
        likes: int
        comments: int

    class BrainrotPostOwner(SQLModel):
        id: int
        username: str

    class BrainrotPostComment(SQLModel):
        id: int
        text: str
        likes_count: int

    class BrainrotPost(SQLModel):
        id: str
        published_on: datetime # timestamp in utc
        title: str | None
        caption: str | None
        accessibility_caption: str | None
        is_sponsored: bool 
        comment_count: int
        owner: BrainrotPostOwner
        engagement: BrainrotPostEngagement
        # comments: list[BrainrotPostComment] | None
    
    return BrainrotPost, BrainrotPostEngagement, BrainrotPostOwner


@app.cell
def _(
    BrainrotPost,
    BrainrotPostEngagement,
    BrainrotPostOwner,
    InstaloaderContext,
    Post,
):
    def get_post_details(instagram_context: InstaloaderContext, reel_code: str):
        try:
            post = Post.from_shortcode(instagram_context, reel_code)

            # get_comments api is down currently
            # https://github.com/instaloader/instaloader/issues/2635
            # todo fix later
            # comments = []
            # for comment in post.get_comments():
            #     id = comment.id
            #     text = comment.text
            #     likes_count = comment.likes_count

            #     comments.append(BrainrotPostComment(
            #         id=id,
            #         text=text,
            #         likes_count=likes_count
            #     ))
        
            return BrainrotPost(
                id=reel_code,
                published_on=post.date_utc,
                title=post.title,
                caption=post.caption,
                accessibility_caption=post.accessibility_caption,
                is_sponsored=post.is_sponsored,
                comment_count=post.comments,
                owner= BrainrotPostOwner(
                    id=post.owner_id,
                    username=post.owner_username
                ),
                engagement=BrainrotPostEngagement(
                    likes=post.likes,
                    comments=post.comments
                ),
                # comments = comments
            )
        except Exception as e:
            print(f"Unable to fetch post : {e}")
            return None
    return (get_post_details,)


@app.cell
def _(get_post_details, ig_loader):
    brainrot_post = get_post_details(ig_loader.context, reel_code="DIthcUDyfb8")
    return (brainrot_post,)


@app.cell
def _(brainrot_post):
    brainrot_post
    return


if __name__ == "__main__":
    app.run()
