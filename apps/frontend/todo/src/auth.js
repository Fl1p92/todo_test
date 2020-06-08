import React from 'react';
import Axios from 'axios';
import {Col, Row, Button, Form, FormGroup, Label, Input, Container} from 'reactstrap';

class Auth extends React.Component {
    state = {
        username: '',
        password: ''
    }
    handleChange = event => this.setState({
        [event.target.name]: event.target.value
    })
    handleSubmit = async event => {
        event.preventDefault()
        const response = await Axios.post(
            'http://localhost/api/v1/auth/', this.state
        )
        localStorage.setItem('refresh_token', response.data.refresh)
        localStorage.setItem('access_token', response.data.access)
    }

    render() {
        return (
            <Container>
                <Form onSubmit={this.handleSubmit}>
                    <Row form>
                        <Col md={6}>
                            <FormGroup>
                                <Label for='username'>Username:</Label>
                                <Input type="text" value={this.state.username} name='username' id='username'
                                       onChange={this.handleChange}/>
                            </FormGroup>
                        </Col>
                        <Col md={6}>
                            <FormGroup>
                                <Label for='password'>Password:</Label>
                                <Input type="password" value={this.state.password} name='password' id='password'
                                       onChange={this.handleChange}/>
                            </FormGroup>
                        </Col>
                    </Row>
                    <Button type="submit" color="info">Login</Button>
                </Form>
            </Container>
        )
    }
}

export default Auth
