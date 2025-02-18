from flask import render_template, request, url_for, redirect, Blueprint, flash
from models import Member
# from peewee import flash

mbp = Blueprint('members', __name__, url_prefix='/members')

@mbp.route('/new-member', methods=['GET', 'POST'])
def new_member():
    if request.method == 'POST':
        return handle_new_member()

    return render_template('memberTemplates/new-member.html')


def handle_new_member():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form.get('address', '')

    try:
        # Create and save a new Member instance
        new_member = Member.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address
        )
        flash("Member added successfully!", "success")
        return redirect(url_for('members.list_member'))
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('new_member'))  # Redirect back to form if there's an error


@mbp.route('/list-member')
def list_member():
    members = Member.select()
    return render_template('memberTemplates/list-member.html', members=members)



@mbp.route('/edit-member/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    member = Member.get_or_none(Member.member_id == member_id)
    if not member:
        flash("Member not found!", "danger")
        return redirect(url_for('members.list_member'))

    if request.method == 'POST':
        return handle_edit_member_post(member)

    return render_template('memberTemplates/edit-member.html', member=member)

def handle_edit_member_post(member):
    member.first_name = request.form['first_name']
    member.last_name = request.form['last_name']
    member.email = request.form['email']
    member.phone = request.form['phone']
    member.address = request.form.get('address', '')
    return update_member(member)

def update_member(member):
    member.save()
    flash("Member updated successfully!", "success")
    return redirect(url_for('members.list_member'))


@mbp.route('/delete-member/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    member = Member.get_or_none(Member.member_id == member_id)
    if member:
        member.delete_instance()
        flash("Member deleted successfully!", "success")
    else:
        flash("Member not found!", "danger")
    return redirect(url_for('members.list_member'))