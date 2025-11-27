from django.shortcuts import render


def home(request):
    return render(request, "website/home.html")




def student_dashboard(request):
    return render(request, 'website/student/dashboard.html')


def student_branches_list(request):
    return render(request, 'website/student/branches/list.html')


def student_spaces_list(request):
    return render(request, 'website/student/spaces/list.html')


def student_bookings_list(request):
    return render(request, 'website/student/bookings/list.html')


def student_bookings_availability(request):
    return render(request, 'website/student/bookings/availability.html')


def student_bookings_confirm(request):
    return render(request, 'website/student/bookings/confirm.html')


def librarian_dashboard(request):
    return render(request, 'website/librarian/dashboard.html')


def librarian_bookings_pending(request):
    return render(request, 'website/librarian/bookings/pending.html')


def librarian_bookings_detail(request):
    return render(request, 'website/librarian/bookings/detail.html')


def librarian_spaces_list(request):
    return render(request, 'website/librarian/spaces/list.html')


def librarian_spaces_edit(request):
    return render(request, 'website/librarian/spaces/edit.html')


def librarian_closures_list(request):
    return render(request, 'website/librarian/closures/list.html')


def librarian_closures_create(request):
    return render(request, 'website/librarian/closures/create.html')


def admin_dashboard(request):
    return render(request, 'website/admin/dashboard.html')


def admin_libraries_list(request):
    return render(request, 'website/admin/libraries/list.html')


def admin_libraries_edit(request):
    return render(request, 'website/admin/libraries/edit.html')


def admin_branches_list(request):
    return render(request, 'website/admin/branches/list.html')


def admin_branches_edit(request):
    return render(request, 'website/admin/branches/edit.html')


def admin_users_assign_librarians(request):
    return render(request, 'website/admin/users/assign_librarians.html')


def admin_settings_system(request):
    return render(request, 'website/admin/settings/system.html')


def reports_dashboard(request):
    return render(request, 'website/reports/dashboard.html')


def reports_usage_totals(request):
    return render(request, 'website/reports/usage/totals.html')


def reports_usage_averages(request):
    return render(request, 'website/reports/usage/averages.html')


def reports_usage_popular_spaces(request):
    return render(request, 'website/reports/usage/popular_spaces.html')


def reports_usage_branch_comparison(request):
    return render(request, 'website/reports/usage/branch_comparison.html')


def bank_dashboard(request):
    return render(request, 'website/bank/dashboard.html')


def bank_payments_list(request):
    return render(request, 'website/bank/payments/list.html')


def bank_payments_update(request):
    return render(request, 'website/bank/payments/update.html')


def user_profile_view(request):
    return render(request, 'website/user/profile/view.html')


def user_profile_edit(request):
    return render(request, 'website/user/profile/edit.html')


def system_audit_logs(request):
    return render(request, 'website/system/audit/logs.html')


def system_errors_branch_closed(request):
    return render(request, 'website/system/errors/branch_closed.html')


def system_errors_conflict(request):
    return render(request, 'website/system/errors/conflict.html')
