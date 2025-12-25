from rest_framework import serializers
from apps.action.models.comment_model import PostComment


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ['post', 'text', 'parent', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        user = self.context['request'].user
        post = data['post']
        parent = data.get('parent')

        user_comments_count = PostComment.objects.filter(user=user, post=post).count()
        if user_comments_count >= 10:
            raise serializers.ValidationError("Only 10 users can comment on this post.")

        if parent:
            if parent.post != post:
                raise serializers.ValidationError("you can't comment on someone else's post. ")

            if parent.parent :
                raise serializers.ValidationError("You can't relpy anymore! ")

        return data
