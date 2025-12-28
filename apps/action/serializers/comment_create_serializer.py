from rest_framework import serializers
from apps.action.models.comment_model import Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    """
        Handles the validation and creation of comments.

        Validation Logic:
        1. Limit: Max 10 comments per user per post.
        2. Context: Ensures reply (parent) belongs to the same post.
        3. Depth: Restricts replies to a maximum of one level (no nested replies).
    """

    class Meta:
        model = Comment
        fields = ['post', 'text', 'parent', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        user = self.context['request'].user
        post = data['post']
        parent = data.get('parent')

        user_comments_count = Comment.objects.filter(user=user, post=post).count()
        if user_comments_count >= 10:
            raise serializers.ValidationError("Only 10 users can comment on this post.")

        if parent:
            if parent.post != post:
                raise serializers.ValidationError("you can't comment on someone else's post. ")

            if parent.parent:
                raise serializers.ValidationError("You can't relpy anymore! ")

        return data
