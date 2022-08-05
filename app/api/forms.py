# -*- coding: utf-8 -*-
from django import forms


class resetPassword(forms.Form):
    new_password = forms.CharField(
        label="新密碼",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '輸入新密碼'
        }))
    re_new_password = forms.CharField(
        label="確認密碼",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '確認新密碼'
        }))
