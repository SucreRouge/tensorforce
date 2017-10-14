# Copyright 2017 reinforce.io. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from tensorforce.agents import BatchAgent
from tensorforce.models import PGLRModel


class TRPOAgent(BatchAgent):
    """
    Trust Region Policy Optimization ([Schulman et al., 2015](https://arxiv.org/abs/1502.05477)) agent.

    ### Configuration options

    #### General:

    * `scope`: TensorFlow variable scope name (default: 'trpo')

    #### Hyperparameters:

    * `batch_size`: Positive integer (**mandatory**)
    * `learning_rate`: Max KL divergence, positive float (default: 1e-2)
    * `discount`: Positive float, at most 1.0 (default: 0.99)
    * `entropy_regularization`: None or positive float (default: none)
    * `gae_lambda`: None or float between 0.0 and 1.0 (default: none)
    * `normalize_rewards`: Boolean (default: false)
    * `likelihood_ratio_clipping`: None or positive float (default: none)

    #### Baseline:

    * `baseline_mode`: None, or one of 'states' or 'network' specifying the network input (default: none)
    * `baseline`: None or specification dict, or per-state specification for aggregated baseline (default: none)
    * `baseline_optimizer`: None or specification dict (default: none)

    #### Pre-/post-processing:

    * `state_preprocessing`: None or dict with (default: none)
    * `exploration`: None or dict with (default: none)
    * `reward_preprocessing`: None or dict with (default: none)

    #### Logging:

    * `log_level`: Logging level, one of the following values (default: 'info')
        + 'info', 'debug', 'critical', 'warning', 'fatal'

    #### TensorFlow Summaries:
    * `summary_logdir`: None or summary directory string (default: none)
    * `summary_labels`: List of summary labels to be reported, some possible values below (default: 'total-loss')
        + 'total-loss'
        + 'losses'
        + 'variables'
        + 'activations'
        + 'relu'
    * `summary_frequency`: Positive integer (default: 1)
    """

    default_config = dict(
        # Agent
        preprocessing=None,
        exploration=None,
        reward_preprocessing=None,
        # BatchAgent
        keep_last_timestep=True,  # not documented!
        # TRPOAgent
        learning_rate=1e-2,
        # Model
        scope='trpo',
        discount=0.99,
        # DistributionModel
        distributions=None,  # not documented!!!
        entropy_regularization=None,
        # PGModel
        baseline_mode=None,
        baseline=None,
        baseline_optimizer=None,
        gae_lambda=None,
        normalize_rewards=False,
        # PGLRModel
        likelihood_ratio_clipping=None,
        # Logging
        log_level='info',
        # TensorFlow Summaries
        summary_logdir=None,
        summary_labels=['total-loss'],
        summary_frequency=1
    )

    # missing: batch agent configs
    # missing: ls_override, ls_accept_ratio, ls_max_backtracks, cg_damping, cg_iterations

    def __init__(self, states_spec, actions_spec, network_spec, config):
        self.network_spec = network_spec
        config = config.copy()
        config.default(self.__class__.default_config)
        config.obligatory(
            optimizer=dict(
                type='optimized_step',
                optimizer=dict(
                    type='natural_gradient',
                    learning_rate=config.learning_rate
                )
            )
        )
        super(TRPOAgent, self).__init__(states_spec, actions_spec, config)

    def initialize_model(self, states_spec, actions_spec, config):
        return PGLRModel(
            states_spec=states_spec,
            actions_spec=actions_spec,
            network_spec=self.network_spec,
            config=config
        )
