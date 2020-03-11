import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';


function GpButton(props) { // general purpose button styled
    return <button
        onClick={props.onClick}
        className="general_purpose">
            {props.text}
        </button>;
}


class TrialView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            state: "idle", // idle, active
            buffer: [], // buffer for sensor readings
        };
    }

    render() {
        if (this.state.state === "idle") {
            return <p>this is an idle tiral</p>;
        }
    }
}


class InitMenu extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            state: "init",
        };
    }

    render() {
        return <p>this is InitMenu</p>;
    }
}


class Main extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            state: "init", // states: init, trial
        }
    }

    render() {
        if (this.state.state === "init") {
            return <InitMenu />;
        }
        else if (this.state.state === "trial") {
            return <TrialView />;
        }
    }
}


ReactDOM.render(<Main />, document.getElementById('root'));
