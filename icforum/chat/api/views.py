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

from rest_framework import viewsets, permissions
from ..models import *
from .serializers import *
from .permissions import *

class RoomViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows rooms to be viewed or edited.
	"""
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, RoomPermission,)

	def get_queryset(self):
		return Room.objects.filter(members=self.request.user)

	def get_serializer_class(self):
		if self.action == 'list' or self.action == 'retrieve':
			return RoomOutputSerializer
		return RoomInputSerializer

class ChatMessageViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows chat messages to be viewed or edited.
	"""
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, ChatMessagePermission,)

	def get_queryset(self):
		return ChatMessage.objects.filter(room__members=self.request.user).order_by('date')

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

	def get_serializer_class(self):
		if self.action == 'list' or self.action == 'retrieve':
			return ChatMessageOutputSerializer
		return ChatMessageInputSerializer