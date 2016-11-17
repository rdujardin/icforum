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

from rest_framework import permissions

class RoomPermission(permissions.BasePermission):
	"""
	Custom permission to allow only members of a room to see it.
	"""

	def has_object_permission(self, request, view, obj):
		return request.user in obj.members.all()

class ChatMessagePermission(permissions.BasePermission):
	"""
	Custom permission to allow only members of a room to post in it and allow only authors to edit their messages.
	"""

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return request.user in obj.room.members.all()

		return obj.author == request.user and request.user in obj.room.members.all()
