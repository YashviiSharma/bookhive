from flask import render_template, request, url_for, redirect, Blueprint, flash
from models import supabase

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
        # Insert new member into Supabase
        response = supabase.table('members').insert({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'address': address
        }).execute()

        print(response)
        flash("Member added successfully!", "success")
        return redirect(url_for('members.list_member'))
    except Exception as e:
        print(f"Error: {str(e)}")
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('members.new_member'))


@mbp.route('/list-member')
def list_member():
    try:
        # Fetch all members from Supabase
        response = supabase.table('members').select('*').execute()
        members = response.data
    except Exception as e:
        print(f"Error: {str(e)}")
        flash(f"Error fetching members: {str(e)}", "danger")
        members = []

    return render_template('memberTemplates/list-member.html', members=members)


@mbp.route('/edit-member/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    try:
        # Get member details from Supabase
        response = supabase.table('members').select('*').eq('member_id', member_id).single().execute()
        member = response.data if not response.error else None

        if not member:
            flash("Member not found!", "danger")
            return redirect(url_for('members.list_member'))

        if request.method == 'POST':
            return handle_edit_member_post(member)

    except Exception as e:
        print(f"Error: {str(e)}")
        flash(f"Error fetching member: {str(e)}", "danger")
        return redirect(url_for('members.list_member'))

    return render_template('memberTemplates/edit-member.html', member=member)


def handle_edit_member_post(member):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form.get('address', '')

    return update_member(member['member_id'], first_name, last_name, email, phone, address)


def update_member(member_id, first_name, last_name, email, phone, address):
    try:
        # Update member in Supabase
        response = supabase.table('members').update({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'address': address
        }).eq('member_id', member_id).execute()

        if response.error:
            raise Exception(response.error.message)

        flash("Member updated successfully!", "success")
    except Exception as e:
        print(f"Error: {str(e)}")
        flash(f"Error updating member: {str(e)}", "danger")

    return redirect(url_for('members.list_member'))


@mbp.route('/delete-member/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    try:
        # Delete member from Supabase
        response = supabase.table('members').delete().eq('member_id', member_id).execute()

        if response.error:
            raise Exception(response.error.message)

        flash("Member deleted successfully!", "success")
    except Exception as e:
        print(f"Error: {str(e)}")
        flash(f"Error deleting member: {str(e)}", "danger")

    return redirect(url_for('members.list_member'))
