'use strict';

class gardencomponent {

    constructor(objectproxy, $state, $rootScope) {
        this.op = objectproxy;
        this.state = $state;
        this.rootscope = $rootScope;

        let self = this;
    }
}

gardencomponent.$inject = ['objectproxy', '$state', '$rootScope'];

export default gardencomponent;
