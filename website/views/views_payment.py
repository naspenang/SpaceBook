import uuid
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from website.models import Booking


@login_required
def fpx_start(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.using("main"),
        id=booking_id,
        user=request.user
    )

    # block double payment
    if booking.payment_status == "PAID":
        return redirect("my_bookings")

    banks = [
        "Maybank",
        "CIMB Bank",
        "Bank Islam",
        "RHB Bank",
        "Public Bank",
    ]

    if request.method == "POST":
        booking.transaction_ref = f"FPX-{uuid.uuid4().hex[:10].upper()}"
        booking.save()
        return redirect("fpx_bank", booking_id=booking.id)

    return render(request, "website/fpx/fpx_start.html", {
        "booking": booking,
        "banks": banks,
    })


@login_required
def fpx_bank(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.using("main"),
        id=booking_id,
        user=request.user
    )

    # block double payment
    if booking.payment_status == "PAID":
        return redirect("my_bookings")

    if request.method == "POST":
        booking.payment_status = "PAID"
        booking.paid_at = now()
        booking.save()
        return redirect("my_bookings")

    return render(request, "website/fpx/fpx_bank.html", {
        "booking": booking
    })
