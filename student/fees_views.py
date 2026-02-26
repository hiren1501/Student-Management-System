from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from student.fees_models import StudentFees

@login_required
@user_passes_test(lambda u: u.is_staff)
def student_fees_list(request):
    """Display all student fees"""
    fees = StudentFees.objects.all().order_by('grade')
    
    if request.method == "POST":
        grade = request.POST.get('grade')
        fees_amount = request.POST.get('fees')
        payment_method = request.POST.get('payment_method')
        
        try:
            # Check if fees for this grade already exists
            existing_fee = StudentFees.objects.filter(grade=grade).first()
            if existing_fee:
                messages.warning(request, f'Fees for Grade {grade} already exists. Please use the Edit option to update.')
            else:
                StudentFees.objects.create(
                    grade=grade,
                    fees=fees_amount,
                    payment_method=payment_method
                )
                messages.success(request, f'Fees for Grade {grade} added successfully!')
            return redirect('student_fees_list')
        except Exception as e:
            messages.error(request, f'Error adding fees: {str(e)}')
    
    return render(request, "student_fees.html", {'fees': fees})


@login_required
@user_passes_test(lambda u: u.is_staff)
def student_fees_update(request, pk):
    """Update existing student fees"""
    fee = get_object_or_404(StudentFees, pk=pk)
    
    if request.method == "POST":
        fee.fees = request.POST.get('fees')
        fee.payment_method = request.POST.get('payment_method')
        
        try:
            fee.save()
            messages.success(request, f'Fees for {fee.get_grade_display_custom()} updated successfully!')
            return redirect('student_fees_list')
        except Exception as e:
            messages.error(request, f'Error updating fees: {str(e)}')
    
    return render(request, "student_fees_update.html", {'fee': fee})


@login_required
@user_passes_test(lambda u: u.is_staff)
def student_fees_delete(request, pk):
    """Delete student fees"""
    fee = get_object_or_404(StudentFees, pk=pk)
    
    try:
        grade_display = fee.get_grade_display_custom()
        fee.delete()
        messages.success(request, f'Fees for {grade_display} deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting fees: {str(e)}')
    
    return redirect('student_fees_list')
