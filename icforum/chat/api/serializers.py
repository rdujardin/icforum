# Copyright 2016 Infinite Connection
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from rest_framework import serializers
from ..models import *
from users.api.serializers import UserSerializer

class RoomInputSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = ('id', 'name', 'members')

class RoomOutputSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = ('id', 'name', 'members')
	
	members = UserSerializer(many=True)

class ChatMessageInputSerializer(serializers.ModelSerializer):
	class Meta:
		model = ChatMessage
		fields = ('id', 'room', 'author', 'date', 'content')

	date = serializers.ReadOnlyField()
	author = serializers.ReadOnlyField(source='author.pk')

class ChatMessageOutputSerializer(serializers.ModelSerializer):
	class Meta:
		model = ChatMessage
		fields = ('id', 'room', 'author', 'date', 'content')

	date = serializers.ReadOnlyField()
	author = UserSerializer(read_only=True)
