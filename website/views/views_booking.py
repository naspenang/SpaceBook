from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count

from website.models import LibrarySpace, Booking
from website.forms.forms_booking import BookingForm


# -----------------------------
# Create booking
# -----------------------------
@login_required
def booking_create(request, space_id):
    space = get_object_or_404(
        LibrarySpace.objects.using("main"),
        space_id=space_id
    )

    if not space.is_active:
        return redirect("space_detail", space_id=space.space_id)

    if request.method == "POST":
        form = BookingForm(request.POST, space=space)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.space = space

            if space.requires_approval:
                booking.status = "PENDING"
            else:
                booking.status = "APPROVED"

            # payment flags
            if space.requires_payment:
                booking.payment_status = "UNPAID"

            booking.save()
            return redirect("space_detail", space_id=space.space_id)
    else:
        form = BookingForm(space=space)

    return render(request, "website/booking/booking_form.html", {
        "form": form,
        "space": space,
    })


# -----------------------------
# My bookings (user)
# -----------------------------
@login_required
def my_bookings(request):
    bookings = (
        Booking.objects.using("main")
        .select_related("space", "space__library")
        .filter(user=request.user)
        .order_by("-created_at")
    )

    return render(request, "website/booking/my_bookings.html", {
        "bookings": bookings,
    })


# -----------------------------
# Cancel booking (user)
# -----------------------------
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.using("main"),
        id=booking_id,
        user=request.user
    )

    if booking.status not in ["CANCELLED", "REJECTED"]:
        booking.status = "CANCELLED"
        booking.save()
        messages.success(request, "Booking has been cancelled.")

    return redirect("my_bookings")


# -----------------------------
# Pending bookings (librarian)
# -----------------------------
@login_required
def pending_bookings(request):
    if not request.user.is_staff:
        return redirect("my_bookings")

    bookings = (
        Booking.objects.using("main")
        .select_related("space", "space__library")
        .filter(status="PENDING")
        .order_by("booking_date", "start_time")
    )

    return render(request, "website/booking/pending_bookings.html", {
        "bookings": bookings,
    })


# -----------------------------
# Approve booking (librarian)
# -----------------------------
@login_required
def approve_booking(request, booking_id):
    if not request.user.is_staff:
        return redirect("my_bookings")

    booking = get_object_or_404(
        Booking.objects.using("main"),
        id=booking_id,
        status="PENDING"
    )

    booking.status = "APPROVED"
    booking.save()

    messages.success(request, "Booking approved.")
    return redirect("pending_bookings")


# -----------------------------
# Reject booking (librarian)
# -----------------------------
@login_required
def reject_booking(request, booking_id):
    if not request.user.is_staff:
        return redirect("my_bookings")

    booking = get_object_or_404(
        Booking.objects.using("main"),
        id=booking_id,
        status="PENDING"
    )

    booking.status = "REJECTED"
    booking.save()

    messages.warning(request, "Booking rejected.")
    return redirect("pending_bookings")


# -----------------------------
# Booking report (librarian)
# -----------------------------
@login_required
def booking_report(request):
    if not request.user.is_staff:
        return redirect("my_bookings")

    qs = (
        Booking.objects.using("main")
        .select_related("space", "space__library")
    )

    # Date range filtering
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date:
        qs = qs.filter(booking_date__gte=start_date)

    if end_date:
        qs = qs.filter(booking_date__lte=end_date)

    # Summary
    summary = {
        "total": qs.count(),
        "approved": qs.filter(status="APPROVED").count(),
        "pending": qs.filter(status="PENDING").count(),
        "cancelled": qs.filter(status="CANCELLED").count(),
        "paid": qs.filter(payment_status="PAID").count(),
        "unpaid": qs.filter(payment_status="UNPAID").count(),
    }

    # Per-space usage
    space_usage = (
        qs.values(
            "space__space_name",
            "space__library__library_name"
        )
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    top_spaces = space_usage[:5]

    return render(request, "website/booking/booking_report.html", {
        "bookings": qs.order_by("-booking_date", "-start_time"),
        "summary": summary,
        "space_usage": space_usage,
        "top_spaces": top_spaces,
        "start_date": start_date,
        "end_date": end_date,
    })
