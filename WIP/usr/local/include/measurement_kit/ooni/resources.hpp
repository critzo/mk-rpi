// Part of measurement-kit <https://measurement-kit.github.io/>.
// Measurement-kit is free software under the BSD license. See AUTHORS
// and LICENSE for more information on the copying conditions.
#ifndef MEASUREMENT_KIT_OONI_RESOURCES_HPP
#define MEASUREMENT_KIT_OONI_RESOURCES_HPP

#include <measurement_kit/common.hpp>
#include <measurement_kit/ext.hpp>

namespace mk {
namespace ooni {
namespace resources {

void get_latest_release(Callback<Error, std::string> callback,
                        Settings settings = {},
                        SharedPtr<Reactor> reactor = Reactor::global(),
                        SharedPtr<Logger> logger = Logger::global());

void get_manifest_as_json(std::string version,
                          Callback<Error, Json> callback,
                          Settings settings = {},
                          SharedPtr<Reactor> reactor = Reactor::global(),
                          SharedPtr<Logger> logger = Logger::global());

void get_resources_for_country(std::string latest,
                               Json manifest,
                               std::string country,
                               Callback<Error> callback,
                               Settings settings = {},
                               SharedPtr<Reactor> reactor = Reactor::global(),
                               SharedPtr<Logger> logger = Logger::global());

void get_resources(std::string latest, std::string country,
                   Callback<Error> callback, Settings settings = {},
                   SharedPtr<Reactor> reactor = Reactor::global(),
                   SharedPtr<Logger> logger = Logger::global());

} // namespace resources
} // namespace mk
} // namespace ooni
#endif
