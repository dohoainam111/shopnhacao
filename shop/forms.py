from django import forms
from .models import OrderRequest

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Field cho phép chọn nhiều file ảnh cùng lúc trong 1 lần bấm."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"multiple": True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
class OrderRequestForm(forms.ModelForm):
    # Honeypot: field ẩn với CSS, người dùng thật sẽ không thấy/không điền.
    # Bot tự động điền form thường điền vào mọi field kể cả field ẩn -> nếu có giá trị thì coi là spam.
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "hp-field", "tabindex": "-1", "autocomplete": "off"}),
        label="",
    )


    class Meta:
        model = OrderRequest
        fields = ["customer_name", "phone", "address", "note"]
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Họ và tên"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Số điện thoại (VD: 0912345678)"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Địa chỉ nhận hàng"}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Ghi chú (nếu có)"}),
        }
        labels = {
            "customer_name": "Họ và tên",
            "phone": "Số điện thoại",
            "address": "Địa chỉ",
            "note": "Ghi chú",
        }

    def is_honeypot_triggered(self):
        return bool(self.cleaned_data.get("website"))
