from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Equipment, Member 
from app.forms import RegistrationForm, EquipmentForm, LoginForm, MemberForm, EditMemberForm, DeleteMemberForm, EditEquipmentForm
from urllib.parse import urlparse
import os
import secrets
from flask import current_app


#ホームページ
def init_routes(app):
    @app.route('/')
    @app.route('/index')
    @login_required
    def index():
        return render_template('index.html', title='Home')

    #ユーザー登録
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('登録が完了しました')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)

    # ログイン
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        return render_template('login.html', title='Sign In', form=form)

    #ログアウト
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    #備品リスト
    @app.route("/equipment_list")
    @login_required
    def equipment_list():
        search = request.args.get('search', '')
        assembled_bows = Equipment.query.filter_by(category='assembled_bow').all()
        cases = Equipment.query.filter_by(category='case').all()
        arrows = Equipment.query.filter_by(category='arrow').all()
        parts = Equipment.query.filter_by(category='parts').all()
        other_equipment = Equipment.query.filter_by(category='other').all()
        edit_form = EditEquipmentForm()
        
        # 数量が1より大きい場合、その数だけ備品を複製
        for category in [assembled_bows, cases, arrows, parts, other_equipment]:
            expanded_category = []
            for item in category:
                for _ in range(item.quantity):
                    expanded_category.append(item)
            category[:] = expanded_category

        return render_template('equipment_list.html', 
                            title='Equipment List',
                            assembled_bows=assembled_bows,
                            cases=cases,
                            arrows=arrows,
                            parts=parts,
                            other_equipment=other_equipment,
                            form=edit_form,
                            search=search)
        
    #備品情報取得API
    @app.route('/api/equipment/<int:equipment_id>')
    @login_required
    def get_equipment(equipment_id):
        equipment = Equipment.query.get_or_404(equipment_id)
        return jsonify({
            'id': equipment.id,
            'name': equipment.name,
            'category': equipment.category,
            'condition': equipment.condition,
            'user_id': equipment.user_id,
            'details': equipment.details,
        })
    
    #備品追加
    @app.route("/add_equipment", methods=['GET', 'POST'])
    @login_required
    def add_equipment():
        form = EquipmentForm()
        if form.validate_on_submit():
            quantity = form.quantity.data
            for _ in range(quantity):
                equipment = Equipment(
                    name=form.name.data,
                    category=form.category.data,
                    condition=form.condition.data,
                    user_id=form.user.data if form.user.data != 0 else None,
                    details=form.details.data
                )
                db.session.add(equipment)
            db.session.commit()
            flash(f'{quantity} item(s) have been added!', 'success')
            return redirect(url_for('equipment_list'))
        return render_template('add_equipment.html', title='Add Equipment', form=form)
    
    #備品編集
    @app.route("/edit_equipment/<int:equipment_id>", methods=['GET', 'POST'])
    @login_required
    def edit_equipment(equipment_id):
        equipment = Equipment.query.get_or_404(equipment_id)
        form = EditEquipmentForm(obj=equipment)
        if form.validate_on_submit():
            equipment.name = form.name.data
            equipment.category = form.category.data
            equipment.condition = form.condition.data
            equipment.user_id = form.user.data if form.user.data != 0 else None
            equipment.details = form.details.data
            equipment.quantity = form.quantity.data
            db.session.commit()
            flash('Equipment has been updated!', 'success')
            return redirect(url_for('equipment_list'))
        return render_template('edit_equipment.html', title='Edit Equipment', form=form, equipment=equipment)
    
    #備品削除
    @app.route("/delete_equipment/<int:equipment_id>", methods=['POST'])
    @login_required
    def delete_equipment(equipment_id):
        equipment = Equipment.query.get_or_404(equipment_id)
        db.session.delete(equipment)
        db.session.commit()
        flash('Equipment has been deleted!', 'success')
        return redirect(url_for('equipment_list'))
        
    #メンバー追加
    @app.route("/add_member", methods=['GET', 'POST'])
    @login_required
    def add_member():
        form = MemberForm()
        if form.validate_on_submit():
            member = Member(name=form.name.data)
            db.session.add(member)
            db.session.commit()
            flash('New member has been added!', 'success')
            return redirect(url_for('member_list'))
        return render_template('add_member.html', title='Add Member', form=form)
    
    #メンバーリスト表示
    @app.route("/member_list", methods=['GET', 'POST'])
    @login_required
    def member_list():
        members = Member.query.order_by(Member.name).all()
        add_form = MemberForm()
        edit_form = EditMemberForm()
        delete_form = DeleteMemberForm()

        if add_form.validate_on_submit():
            member = Member(name=add_form.name.data)
            db.session.add(member)
            db.session.commit()
            flash('New member has been added!', 'success')
            return redirect(url_for('member_list'))

        return render_template('member_list.html', title='Member List', members=members,
                            add_form=add_form, edit_form=edit_form, delete_form=delete_form)
    
    #メンバー編集
    @app.route("/edit_member/<int:member_id>", methods=['POST'])
    @login_required
    def edit_member(member_id):
        member = Member.query.get_or_404(member_id)
        form = EditMemberForm()
        if form.validate_on_submit():
            member.name = form.name.data
            db.session.commit()
            flash('Member has been updated!', 'success')
        else:
            flash('Failed to update member.', 'danger')
        return redirect(url_for('member_list'))

    #メンバー削除
    @app.route("/delete_member/<int:member_id>", methods=['POST'])
    @login_required
    def delete_member(member_id):
        member = Member.query.get_or_404(member_id)
        try:
            db.session.delete(member)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Member deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    
    return app