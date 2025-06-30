# Understanding Plays, Tasks, and Roles in Ansible

## Overview

This document explains the difference between **plays**, **tasks**, and **roles** in Ansible, how they relate to each other, and how to use them effectively in a playbook.

---

## Plays

* A **play** maps a group of hosts to roles or tasks.
* It is the **top-level unit** in a playbook.
* Each play defines:

  * Target hosts (`hosts`)
  * Variables (`vars`)
  * Privilege escalation (`become`)
  * One or more **tasks** or **roles**

### Example:

```yaml
- name: Install and configure web server
  hosts: webservers
  become: yes

  tasks:
    - name: Install Nginx
      apt:
        name: nginx
        state: present
```

---

## Tasks

* A **task** is a single unit of work.
* Each task calls one Ansible module to perform a specific action.
* Tasks are defined **inside a play** or **inside a role**.

### Example:

```yaml
- name: Install Nginx
  apt:
    name: nginx
    state: present
```

---

## Roles

* **Roles** are a structured way to organize Ansible code into reusable components.
* Called from within **plays**.
* Roles automatically load files from their own standardized directories.

### Example Playbook Using Roles:

```yaml
- name: Deploy web application
  hosts: app_servers
  become: true

  roles:
    - common
    - nginx
    - { role: app_deploy, app_name: myapp }
```

### Role Directory Structure:

```
roles/
  nginx/
    tasks/
      main.yml
    handlers/
      main.yml
    templates/
      nginx.conf.j2
    files/
      index.html
    vars/
      main.yml
    defaults/
      main.yml
    meta/
      main.yml
```

---

## Summary Table

| Element  | Description                            | Scope                   | Contains                                 |
| -------- | -------------------------------------- | ----------------------- | ---------------------------------------- |
| **Play** | Applies a set of tasks to a host/group | Top-level in a playbook | One or more tasks or roles               |
| **Task** | Executes a specific action             | Inside a play or a role | Uses Ansible module                      |
| **Role** | Reusable collection of automation code | Called inside a play    | Has its own tasks, vars, templates, etc. |

---

## Why Use Roles?

* **Reusability**: Use across different playbooks.
* **Organization**: Clean and structured code.
* **Portability**: Easily shared or published (e.g., Ansible Galaxy).

---


