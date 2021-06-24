import React from "react";
import axios from 'axios'

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      first_name: '',
      last_name: '',
      user_name: '',
      email: '',
      password: '',
      id: 0,
      users: []
    }
  }
  componentDidMount() {
    axios.get(`http://localhost:5000/get`)
      .then(res => {
        console.log(res.data)
        this.setState({
          first_name: '',
          last_name: '',
          user_name: '',
          email: '',
          password: '',
          id: 0,
          users: res.data
        })
      })
  }
  first_name_change = event => (
    this.setState({
      first_name: event.target.value
    })
  )
  last_name_change = event => (
    this.setState({
      last_name: event.target.value
    })
  )
  user_name_change = event => (
    this.setState({
      user_name: event.target.value
    })
  )
  email_change = event => (
    this.setState({
      email: event.target.value
    })
  )
  password_change = event => (
    this.setState({
      password: event.target.value
    })
  )
  delete(e,id) {
    axios.delete(`http://localhost:5000/delete/${id}`)
      .then(res => {
        console.log(res.data)
        this.componentDidMount()
      })
  }
  submit(e, id) {
    e.preventDefault()
    if (id === 0) {
      axios.post(`http://localhost:5000/post`, {
        'first_name': this.state.first_name,
        'last_name': this.state.last_name,
        'user_name': this.state.user_name,
        'email': this.state.email,
        'password': this.state.password,
      }).then(res => {
        console.log(res.data)
        this.componentDidMount()
      })
    } else {
      axios.put(`http://localhost:5000/put/${id}`, {
        'first_name': this.state.first_name,
        'last_name': this.state.last_name,
        'user_name': this.state.user_name,
        'email': this.state.email,
        'password': this.state.password,
      }).then(res => {
        console.log(res.data)
        this.componentDidMount()
      })
    }

  }
  editget(e, id) {
    axios.get(`http://localhost:5000/get/${id}`)
      .then(res => {
        this.setState({
          first_name: res.data.first_name,
          last_name: res.data.last_name,
          user_name: res.data.user_name,
          email: res.data.email,
          password: res.data.password,
          id: res.data.id
        })
      })
  }

  render() {
    return (
      <div className="row">
        <div className="col-lg-6">
          <form onSubmit={(e) => this.submit(e, this.state.id)}>
            <div className="form-group">
              <input className="form-control" required="True"type="text" value={this.state.first_name} placeholder="First_name" onChange={(e) => this.first_name_change(e)} />
            </div>
            <div className="form-group">
              <input className="form-control" required="True"type="text" value={this.state.last_name} placeholder="Last_name" onChange={(e) => this.last_name_change(e)} />
            </div>
            <div className="form-group">
              <input className="form-control" required="True"type="text" value={this.state.user_name} placeholder="User_name" onChange={(e) => this.user_name_change(e)} />
            </div>
            <div className="form-group">
              <input className="form-control" required="True"type="email" value={this.state.email} placeholder="Email" onChange={(e) => this.email_change(e)} />
            </div>
            <div className="form-group">
              <input className="form-control" required="True" type="password" value={this.state.password} placeholder="Password" onChange={(e) => this.password_change(e)} />
            </div>
            <div className="form-group">
              <button type="submit" className="btn btn-block btn-outline-success">Submit</button>
            </div>
          </form>
        </div>
        <div className="col-lg-6">
          <table className="table">
            <tbody>
              {this.state.users.map(user =>

                <tr key={user.id}>
                  <td>{user.first_name}</td>
                  <td>{user.last_name}</td>
                  <td>{user.user_name}</td>
                  <td>{user.email}</td>
                  <td>{user.password}</td>
                  <td>
                    <button onClick={(e) => this.delete(e, user.id)} className="btn btn-outline-danger btn-sm">Delete</button>
                  </td>
                  <td>
                    <button onClick={(e) => this.editget(e, user.id)} className="btn btn-outline-dark btn-sm">Edit</button>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    )
  }
}

export default App;